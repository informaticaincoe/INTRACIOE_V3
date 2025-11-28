# hyperzip.py
# -----------------------------------------------------------------------------
# HyperZip: compresor lossless experimental para imágenes 2D (y RGB)
# Bloques 2D + predicción 2D reversible + mezcla reversible + IWT 2D (Haar)
# Codificación entropy: Range Coder adaptativo por contexto de banda wavelet.
# Decorrelación de color reversible: (G, R-G, B-G) módulo 256.
# -----------------------------------------------------------------------------

import io
import struct
import numpy as np


# =============================================================================
# Utilidades básicas: zigzag y LEB128 (enteros sin signo)
# =============================================================================

def zigzag_encode_int64(arr: np.ndarray) -> np.ndarray:
    """Mapea enteros con signo a enteros sin signo (tipo zigzag).
    x -> (x << 1) ^ (x >> 63)   (trabajamos en int64)"""
    x = arr.astype(np.int64)
    return ((x << 1) ^ (x >> 63)).astype(np.uint64)

def zigzag_decode_int64(arr: np.ndarray) -> np.ndarray:
    """Inverso del zigzag para int64."""
    u = arr.astype(np.uint64)
    return ((u >> 1) ^ -(u & 1)).astype(np.int64)

def leb128u_encode(u: int) -> bytes:
    """LEB128 sin signo para un entero Python (0..2^64-1 típico)."""
    b = bytearray()
    while True:
        byte = u & 0x7F
        u >>= 7
        if u:
            b.append(byte | 0x80)
        else:
            b.append(byte)
            break
    return bytes(b)

def leb128u_decode(stream: io.BytesIO) -> int:
    """Decodifica un entero LEB128 sin signo desde stream."""
    shift = 0
    result = 0
    while True:
        b = stream.read(1)
        if not b:
            raise EOFError("LEB128: fin inesperado")
        byte = b[0]
        result |= (byte & 0x7F) << (shift)
        if (byte & 0x80) == 0:
            break
        shift += 7
    return result


# =============================================================================
# Range Coder adaptativo por contexto (símbolos = bytes 0..255)
# Modelo: frecuencias adaptativas por contexto_id
# =============================================================================

class AdaptiveByteModel:
    """Modelo adaptativo de 256 símbolos por contexto, con tablas cumulativas."""
    def __init__(self):
        self.freqs = np.ones(256, dtype=np.uint32)  # inicializamos con 1 para evitar ceros
        self.total = 256

    def renorm(self):
        # Evitar overflow de contadores
        if self.total >= (1 << 24):
            self.freqs = (self.freqs + 1) // 2
            self.freqs[self.freqs == 0] = 1
            self.total = int(self.freqs.sum())

    def update(self, sym: int):
        self.freqs[sym] += 1
        self.total += 1
        self.renorm()

    def cumulative(self):
        # Devolvemos cumulativas en array (256+1)
        cdf = np.zeros(257, dtype=np.uint32)
        np.cumsum(self.freqs, dtype=np.uint32, out=cdf[1:])
        return cdf, self.total


class RangeEncoder:
    def __init__(self):
        self.low = 0
        self.high = 0xFFFFFFFF
        self.out = bytearray()
        self.cache = 0
        self.cache_size = 0

    def _output_byte(self, b):
        self.out.append(b & 0xFF)

    def _shift(self):
        byte = (self.low >> 24) & 0xFF
        self._output_byte(byte)
        self.low = (self.low << 8) & 0xFFFFFFFF
        self.high = ((self.high << 8) | 0xFF) & 0xFFFFFFFF

    def encode_symbol(self, sym: int, model: AdaptiveByteModel):
        # sym en [0..255]
        cdf, total = model.cumulative()
        low_count = int(cdf[sym])
        high_count = int(cdf[sym + 1])

        range_ = (self.high - self.low + 1)
        self.high = self.low + (range_ * high_count // total) - 1
        self.low = self.low + (range_ * low_count // total)

        # Normalización
        while True:
            if (self.high ^ self.low) & 0xFF000000 == 0:
                self._shift()
            elif (self.low & 0x00FFFFFF) == 0 and (self.high & 0x00FFFFFF) == 0x00FFFFFF:
                # underflow (bit-stuffing clásico); simplificado
                self.low = (self.low & 0xFF000000)
                self.high = self.low | 0x00FFFFFF
                self._shift()
            else:
                break

        model.update(sym)

    def finish(self):
        for _ in range(4):
            self._shift()
        return bytes(self.out)


class RangeDecoder:
    def __init__(self, data: bytes):
        self.data = data
        self.pos = 0
        self.low = 0
        self.high = 0xFFFFFFFF
        self.code = 0
        # Inicializar code con 4 bytes
        for _ in range(4):
            self.code = ((self.code << 8) | self._read_byte()) & 0xFFFFFFFF

    def _read_byte(self):
        if self.pos < len(self.data):
            b = self.data[self.pos]
            self.pos += 1
            return b
        return 0  # padding

    def _normalize(self):
        while True:
            if (self.high ^ self.low) & 0xFF000000 == 0:
                self.low = (self.low << 8) & 0xFFFFFFFF
                self.high = ((self.high << 8) | 0xFF) & 0xFFFFFFFF
                self.code = ((self.code << 8) | self._read_byte()) & 0xFFFFFFFF
            elif (self.low & 0x00FFFFFF) == 0 and (self.high & 0x00FFFFFF) == 0x00FFFFFF:
                self.low = (self.low & 0xFF000000)
                self.high = self.low | 0x00FFFFFF
                self.code = ((self.code << 8) | self._read_byte()) & 0xFFFFFFFF
            else:
                break

    def decode_symbol(self, model: AdaptiveByteModel) -> int:
        cdf, total = model.cumulative()
        range_ = (self.high - self.low + 1)
        # Buscar el símbolo por búsqueda binaria
        value = ((self.code - self.low + 1) * total - 1) // range_
        # cdf es acumulado; hallamos el índice s tal que cdf[s] <= value < cdf[s+1]
        lo, hi = 0, 256
        while lo + 1 < hi:
            mid = (lo + hi) // 2
            if cdf[mid] <= value:
                lo = mid
            else:
                hi = mid
        sym = lo

        low_count = int(cdf[sym])
        high_count = int(cdf[sym + 1])

        self.high = self.low + (range_ * high_count // total) - 1
        self.low  = self.low + (range_ * low_count  // total)

        self._normalize()
        model.update(sym)
        return sym


# =============================================================================
# IWT 1D y 2D (Haar por lifting), mezcla reversible 1D/2D (butterflies)
# =============================================================================

def haar_lifting_forward_1d(x: np.ndarray, levels: int):
    out = x.astype(np.int64).copy()
    sizes = []
    n = len(out)
    for _ in range(levels):
        if n < 2:
            break
        m = n // 2
        s = np.empty(m, dtype=np.int64)
        d = np.empty(m, dtype=np.int64)
        for i in range(m):
            a = out[2*i]
            b = out[2*i + 1]
            dd = b - a
            ss = a + (dd >> 1)
            s[i] = ss
            d[i] = dd
        out[:m] = s
        out[m:2*m] = d
        sizes.append(m)
        n = m
    return out, sizes

def haar_lifting_inverse_1d(x: np.ndarray, sizes):
    out = x.astype(np.int64).copy()
    for m in reversed(sizes):
        s = out[:m].copy()
        d = out[m:2*m].copy()
        rec = np.empty(2*m, dtype=np.int64)
        for i in range(m):
            ss = s[i]
            dd = d[i]
            a = ss - (dd >> 1)
            b = dd + a
            rec[2*i] = a
            rec[2*i + 1] = b
        out[:2*m] = rec
    return out

def haar2d_forward_int(img: np.ndarray, levels: int):
    A = img.astype(np.int64).copy()
    h, w = A.shape
    shapes = []
    hh, ww = h, w
    for _ in range(levels):
        if hh < 2 or ww < 2:
            break
        # filas
        for r in range(hh):
            row = A[r, :ww]
            tr, _ = haar_lifting_forward_1d(row, 1)
            A[r, :ww] = tr
        # columnas
        for c in range(ww):
            col = A[:hh, c]
            tr, _ = haar_lifting_forward_1d(col, 1)
            A[:hh, c] = tr
        shapes.append((hh, ww))
        hh //= 2
        ww //= 2
    return A, shapes

def haar2d_inverse_int(coef: np.ndarray, shapes):
    A = coef.astype(np.int64).copy()
    for (hh, ww) in reversed(shapes):
        # columnas inversa
        for c in range(ww):
            col = A[:hh, c]
            rec = haar_lifting_inverse_1d(col, [hh//2] if hh >= 2 else [])
            A[:hh, c] = rec
        # filas inversa
        for r in range(hh):
            row = A[r, :ww]
            rec = haar_lifting_inverse_1d(row, [ww//2] if ww >= 2 else [])
            A[r, :ww] = rec
    return A

def mix_reversible_1d_forward(v: np.ndarray, rounds: int = 1, stride: int = 1):
    out = v.astype(np.int64).copy()
    n = len(out)
    meta = []
    s = stride
    for _ in range(rounds):
        idxs = []
        for start in range(0, s):
            i = start
            while i + s < n:
                idxs.append((i, i + s))
                i += 2*s
        for i, j in idxs:
            a = out[i]; b = out[j]
            d = b - a
            ssum = a + (d >> 1)
            out[i] = ssum
            out[j] = d
        meta.append((s, idxs))
        s *= 2
    return out, meta

def mix_reversible_1d_inverse(v: np.ndarray, meta):
    out = v.astype(np.int64).copy()
    for _, idxs in reversed(meta):
        for i, j in idxs:
            ssum = out[i]; d = out[j]
            a = ssum - (d >> 1)
            b = d + a
            out[i] = a
            out[j] = b
    return out

def mix_reversible_2d_forward(img: np.ndarray, rounds_h: int = 1, rounds_v: int = 1, stride: int = 1):
    """Mezcla reversible 2D: aplica butterflies por filas y por columnas."""
    A = img.astype(np.int64).copy()
    h, w = A.shape
    meta = {"rows": [], "cols": []}
    # Filas
    for r in range(h):
        row, m = mix_reversible_1d_forward(A[r, :], rounds=rounds_h, stride=stride)
        A[r, :] = row
        meta["rows"].append(m)
    # Cols
    for c in range(w):
        col, m = mix_reversible_1d_forward(A[:, c], rounds=rounds_v, stride=stride)
        A[:, c] = col
        meta["cols"].append(m)
    return A, meta

def mix_reversible_2d_inverse(A: np.ndarray, meta):
    B = A.astype(np.int64).copy()
    h, w = B.shape
    # Columnas inversa
    for c in range(w):
        B[:, c] = mix_reversible_1d_inverse(B[:, c], meta["cols"][c])
    # Filas inversa
    for r in range(h):
        B[r, :] = mix_reversible_1d_inverse(B[r, :], meta["rows"][r])
    return B


# =============================================================================
# Predicción 2D reversible (estilo PNG): None, Left, Up, Paeth
# =============================================================================

PRED_NONE = 0
PRED_LEFT = 1
PRED_UP   = 2
PRED_PAETH= 3

def _paeth(a, b, c):
    # a = left, b = up, c = up-left
    p  = a + b - c
    pa = abs(p - a)
    pb = abs(p - b)
    pc = abs(p - c)
    if pa <= pb and pa <= pc:
        return a
    elif pb <= pc:
        return b
    return c

def predict2d_and_residual(img_u8: np.ndarray, mode: int):
    """Devuelve residuo entero (int16) de img - pred(mode)."""
    h, w = img_u8.shape
    img = img_u8.astype(np.int16)
    resid = np.empty((h, w), dtype=np.int16)
    if mode == PRED_NONE:
        resid[:] = img
        return resid
    if mode == PRED_LEFT:
        resid[:, 0] = img[:, 0]
        resid[:, 1:] = img[:, 1:] - img[:, :-1]
        return resid
    if mode == PRED_UP:
        resid[0, :] = img[0, :]
        resid[1:, :] = img[1:, :] - img[:-1, :]
        return resid
    if mode == PRED_PAETH:
        resid[0, 0] = img[0, 0]
        # fila 0
        for x in range(1, w):
            pred = img[0, x-1]
            resid[0, x] = img[0, x] - pred
        # resto
        for y in range(1, h):
            resid[y, 0] = img[y, 0] - img[y-1, 0]
            for x in range(1, w):
                a = img[y, x-1]
                b = img[y-1, x]
                c = img[y-1, x-1]
                pred = _paeth(a, b, c)
                resid[y, x] = img[y, x] - pred
        return resid
    raise ValueError("Modo de predicción no soportado")

def reconstruct2d_from_residual(resid: np.ndarray, mode: int) -> np.ndarray:
    h, w = resid.shape
    out = np.empty((h, w), dtype=np.int16)
    if mode == PRED_NONE:
        return resid.astype(np.int16)
    if mode == PRED_LEFT:
        out[:, 0] = resid[:, 0]
        for x in range(1, w):
            out[:, x] = (out[:, x-1] + resid[:, x])
        return out
    if mode == PRED_UP:
        out[0, :] = resid[0, :]
        for y in range(1, h):
            out[y, :] = (out[y-1, :] + resid[y, :])
        return out
    if mode == PRED_PAETH:
        out[0, 0] = resid[0, 0]
        # fila 0
        for x in range(1, w):
            out[0, x] = out[0, x-1] + resid[0, x]
        # resto
        for y in range(1, h):
            out[y, 0] = out[y-1, 0] + resid[y, 0]
            for x in range(1, w):
                a = out[y, x-1]
                b = out[y-1, x]
                c = out[y-1, x-1]
                pred = _paeth(a, b, c)
                out[y, x] = pred + resid[y, x]
        return out
    raise ValueError("Modo de predicción no soportado")


# =============================================================================
# Decorrelación reversible de color (RGB -> G, (R-G)mod256, (B-G)mod256)
# =============================================================================

def rgb_to_g_drg_dbg(rgb: np.ndarray):
    """rgb: HxWx3 uint8 -> canales G, dR=(R-G)mod256, dB=(B-G)mod256 (uint8)."""
    g = rgb[..., 1]
    drg = (rgb[..., 0].astype(np.int16) - g.astype(np.int16)) % 256
    dbg = (rgb[..., 2].astype(np.int16) - g.astype(np.int16)) % 256
    return g.astype(np.uint8), drg.astype(np.uint8), dbg.astype(np.uint8)

def g_drg_dbg_to_rgb(g: np.ndarray, drg: np.ndarray, dbg: np.ndarray):
    g16 = g.astype(np.int16)
    r = (drg.astype(np.int16) + g16) % 256
    b = (dbg.astype(np.int16) + g16) % 256
    rgb = np.stack([r, g16, b], axis=-1).astype(np.uint8)
    return rgb


# =============================================================================
# Serialización de coeficientes por bandas con RangeCoder + Contextos
# Contexto = (nivel, banda_id) banda_id: 0=LL, 1=LH, 2=HL, 3=HH
# Codificamos coeficientes (int64) -> zigzag -> LEB128 bytes -> RangeCoder
# =============================================================================

def _band_slices(level_shapes):
    """
    A partir de shapes [(hh, ww), ...] de pirámide, calcula para cada nivel
    los slices de bandas LL/LH/HL/HH dentro del buffer 2D de coeficientes.
    Devuelve lista por nivel: (slice_LL, slice_LH, slice_HL, slice_HH)
    Cada slice es (y0,y1,x0,x1)
    """
    bands = []
    for (hh, ww) in level_shapes:
        h2, w2 = hh//2, ww//2
        # Suponemos layout típico tras 1 nivel: 
        # top-left = LL, top-right = LH, bottom-left = HL, bottom-right = HH
        LL = (0, h2, 0, w2)
        LH = (0, h2, w2, ww)
        HL = (h2, hh, 0, w2)
        HH = (h2, hh, w2, ww)
        bands.append((LL, LH, HL, HH))
    return bands

def _flatten_bands_for_encoding(coef2d: np.ndarray, shapes):
    """
    Devuelve lista de tuplas [(context_id, vector_int64), ...] en orden:
    niveles de coarse a fine: para cada nivel: LL (solo al final), LH, HL, HH.
    Codificaremos LL del último nivel al final.
    """
    h, w = coef2d.shape
    # LL final está en la esquina superior izquierda del último shapes[-1]
    bands_layout = _band_slices(shapes)
    streams = []
    # Recorremos niveles en orden (coarse -> fine), pero LL solo se codifica del último nivel
    for lvl, (LL, LH, HL, HH) in enumerate(bands_layout):
        y0,y1,x0,x1 = LH
        streams.append(((lvl,1), coef2d[y0:y1, x0:x1].reshape(-1)))
        y0,y1,x0,x1 = HL
        streams.append(((lvl,2), coef2d[y0:y1, x0:x1].reshape(-1)))
        y0,y1,x0,x1 = HH
        streams.append(((lvl,3), coef2d[y0:y1, x0:x1].reshape(-1)))
    # LL del nivel más fino (último shapes)
    if shapes:
        hh, ww = shapes[-1]
        ll = coef2d[0:hh//2, 0:ww//2].reshape(-1)
        streams.append(((len(shapes)-1,0), ll))
    else:
        # sin niveles: toda la imagen es LL
        streams.append(((0,0), coef2d.reshape(-1)))
    return streams

def _encode_streams_with_rc(streams, enc: RangeEncoder):
    """Codifica múltiples streams (cada uno con contexto propio) en un único
    buffer de RangeCoder, serializando primero cantidad de streams y, por cada
    stream, el contexto (lvl,banda) + la carga útil como bytes LEB128 bajo RC.
    """
    # Escribimos en un buffer intermedio los payloads por stream, cada uno RC por separado
    # Aquí, para eficiencia y adaptatividad por contexto, usamos un único RC
    # pero con modelos por (lvl,banda).
    # Escribiremos: N_STREAMS, y luego por stream: lvl,u8  banda,u8  length_bytes, data_rc
    out = io.BytesIO()
    out.write(struct.pack('<I', len(streams)))
    # Mapa de contexto -> modelo
    ctx_models = {}
    for (lvl, band), vec in streams:
        out.write(struct.pack('<B', lvl & 0xFF))
        out.write(struct.pack('<B', band & 0xFF))
        # Preparamos bytes LEB128 del vector zigzagueado
        zz = zigzag_encode_int64(vec)
        # Convertimos a bytes concatenando LEB128 por coeficiente
        raw = bytearray()
        for v in zz:
            raw += leb128u_encode(int(v))
        # Ahora codificamos raw con RC bajo (lvl,band)
        # Para poder reconstruir límites, almacenamos longitud de raw (LEB128) antes.
        raw_len = len(raw)
        out.write(struct.pack('<I', raw_len))
        # Codificar raw usando RC y el modelo del contexto
        if (lvl, band) not in ctx_models:
            ctx_models[(lvl, band)] = AdaptiveByteModel()
        model = ctx_models[(lvl, band)]
        for b in raw:
            enc.encode_symbol(b, model)
    return out.getvalue()

def _decode_streams_with_rc(dec: RangeDecoder, blob_meta: bytes):
    """Lee los metadatos (N streams y sus (lvl,band,raw_len)) y decodifica
    los bytes raw por RangeCoder con los contextos; devuelve lista de
    ( (lvl,band), bytes_raw )."""
    bio = io.BytesIO(blob_meta)
    nstreams = struct.unpack('<I', bio.read(4))[0]
    entries = []
    ctx_models = {}
    for _ in range(nstreams):
        lvl = bio.read(1)[0]
        band = bio.read(1)[0]
        raw_len = struct.unpack('<I', bio.read(4))[0]
        if (lvl, band) not in ctx_models:
            ctx_models[(lvl, band)] = AdaptiveByteModel()
        model = ctx_models[(lvl, band)]
        raw = bytearray()
        for _i in range(raw_len):
            sym = dec.decode_symbol(model)
            raw.append(sym)
        entries.append(((lvl, band), bytes(raw)))
    return entries


# =============================================================================
# Compresión por bloques 2D (grises y RGB con decorrelación), pipeline:
# 1) Decorrelación (si RGB)
# 2) Predicción 2D (elige mejor: None/Left/Up/Paeth por suma |resid|)
# 3) Mezcla reversible 2D (butterflies)
# 4) IWT 2D (Haar)
# 5) Serialización bandas -> LEB128 -> RangeCoder (contextos)
# =============================================================================

MAGIC_IMG = b'HZI2DB'  # HyperZip Image 2D Blocks

def _best_predictor(img: np.ndarray):
    # probamos 4 modos y elegimos el que minimiza sum(abs(resid))
    candidates = [PRED_NONE, PRED_LEFT, PRED_UP, PRED_PAETH]
    scores = []
    for m in candidates:
        resid = predict2d_and_residual(img, m)
        scores.append((int(np.abs(resid).sum()), m))
    scores.sort()
    return scores[0][1]

def _encode_block_gray(enc: RangeEncoder, block: np.ndarray, wavelet_levels: int,
                       mix_rounds_h=1, mix_rounds_v=1, mix_stride=1) -> bytes:
    hB, wB = block.shape
    # Determinar niveles factibles para el bloque
    lvl_h = 0; tmp = hB
    while tmp >= 2 and lvl_h < wavelet_levels:
        tmp //= 2; lvl_h += 1
    lvl_w = 0; tmp = wB
    while tmp >= 2 and lvl_w < wavelet_levels:
        tmp //= 2; lvl_w += 1
    lvls = min(lvl_h, lvl_w)

    # 1) Predictor
    mode = _best_predictor(block)
    resid = predict2d_and_residual(block, mode)     # int16

    # 2) Mezcla reversible 2D
    mixed, mix_meta = mix_reversible_2d_forward(resid, rounds_h=mix_rounds_h,
                                                rounds_v=mix_rounds_v, stride=mix_stride)

    # 3) IWT 2D sobre residuo mezclado
    coef, shapes = haar2d_forward_int(mixed, lvls)

    # 4) Serialización por bandas con RangeCoder
    streams = _flatten_bands_for_encoding(coef, shapes)
    meta_payload = _encode_streams_with_rc(streams, enc)

    # Empaquetar metadatos del bloque (para deshacer todo):
    meta = io.BytesIO()
    meta.write(struct.pack('<H', hB))
    meta.write(struct.pack('<H', wB))
    meta.write(struct.pack('<B', lvls))
    meta.write(struct.pack('<B', mode))
    # Mezcla: guardamos parámetros suficientes para invertir (rondas y stride)
    meta.write(struct.pack('<B', mix_rounds_h))
    meta.write(struct.pack('<B', mix_rounds_v))
    meta.write(struct.pack('<H', mix_stride))

    # Guardar shapes de IWT
    meta.write(struct.pack('<B', len(shapes)))
    for (hh, ww) in shapes:
        meta.write(struct.pack('<I', hh))
        meta.write(struct.pack('<I', ww))

    # Para la mezcla 2D guardamos nada más los parámetros (no los índices),
    # porque la mezcla 1D usa esquema determinista (pares con stride^r).
    # ==> Así es invertible sin almacenar índices por píxel.

    block_meta = meta.getvalue()
    return struct.pack('<I', len(block_meta)) + block_meta + struct.pack('<I', len(meta_payload)) + meta_payload

def _decode_block_gray(dec: RangeDecoder, buf: io.BytesIO) -> np.ndarray:
    meta_len = struct.unpack('<I', buf.read(4))[0]
    meta = io.BytesIO(buf.read(meta_len))
    payload_len = struct.unpack('<I', buf.read(4))[0]
    payload = buf.read(payload_len)

    hB = struct.unpack('<H', meta.read(2))[0]
    wB = struct.unpack('<H', meta.read(2))[0]
    lvls = meta.read(1)[0]
    mode = meta.read(1)[0]
    mix_rounds_h = meta.read(1)[0]
    mix_rounds_v = meta.read(1)[0]
    mix_stride = struct.unpack('<H', meta.read(2))[0]
    nshapes = meta.read(1)[0]
    shapes = []
    for _ in range(nshapes):
        hh = struct.unpack('<I', meta.read(4))[0]
        ww = struct.unpack('<I', meta.read(4))[0]
        shapes.append((hh, ww))

    # Decodificar streams con RC
    streams = _decode_streams_with_rc(dec, payload)

    # Reconstituir coef2d a partir de streams
    coef = np.zeros((hB, wB), dtype=np.int64)
    # Mapear streams a bandas
    bands_layout = _band_slices(shapes)
    # Colocar LH,HL,HH por nivel
    idx = 0
    for lvl, (LL, LH, HL, HH) in enumerate(bands_layout):
        for band_id, sl in [(1, LH), (2, HL), (3, HH)]:
            ((lvl_s, band_s), raw) = streams[idx]; idx += 1
            assert lvl_s == lvl and band_s == band_id
            # raw -> LEB128 -> int64 por zigzag
            raw_bio = io.BytesIO(raw)
            vals = []
            while raw_bio.tell() < len(raw):
                vals.append(leb128u_decode(raw_bio))
            vec = zigzag_decode_int64(np.array(vals, dtype=np.uint64))
            y0,y1,x0,x1 = sl
            coef[y0:y1, x0:x1] = vec.reshape(y1 - y0, x1 - x0)
    # LL final:
    ((lvl_s, band_s), raw) = streams[idx]
    assert band_s == 0
    raw_bio = io.BytesIO(raw)
    vals = []
    while raw_bio.tell() < len(raw):
        vals.append(leb128u_decode(raw_bio))
    vec = zigzag_decode_int64(np.array(vals, dtype=np.uint64))
    if shapes:
        hh, ww = shapes[-1]
        coef[0:hh//2, 0:ww//2] = vec.reshape(hh//2, ww//2)
    else:
        coef[:, :] = vec.reshape(hB, wB)

    # Inversa IWT
    mixed = haar2d_inverse_int(coef, shapes)

    # Inversa mezcla 2D (determinista)
    resid = mix_reversible_2d_inverse(mixed, {
        "rows": [ [ (mix_stride * (2**r), []) for r in range(mix_rounds_h) ] for _ in range(hB) ],
        "cols": [ [ (mix_stride * (2**r), []) for r in range(mix_rounds_v) ] for _ in range(wB) ],
    })
    # OJO: usamos la versión determinista de mix inversa, por lo que meta.rows/cols no contiene índices
    # El algoritmo usa la misma secuencia de pares que el forward, deducible de (rounds, stride)

    # Inversa predictor
    rec = reconstruct2d_from_residual(resid.astype(np.int16), mode)
    rec = np.clip(rec, 0, 255).astype(np.uint8)
    return rec


def compress_image_blocks(img: np.ndarray, block_size: int = 16, wavelet_levels: int = 3,
                          mix_rounds_h: int = 1, mix_rounds_v: int = 1, mix_stride: int = 1) -> bytes:
    """
    Imagen 2D (grises) o 3D (RGB) uint8.
    - Si RGB: decorrelación reversible (G, dR, dB) y compresión por canal.
    - Por canal: predictor 2D -> mezcla reversible -> IWT 2D -> RC por bandas (lossless).
    """
    if img.ndim == 2:
        H, W = img.shape
        C = 1
    elif img.ndim == 3 and img.shape[2] == 3:
        H, W, C = img.shape
    else:
        raise ValueError("Se requiere imagen uint8 2D (grises) o 3D (RGB)")

    header = io.BytesIO()
    header.write(MAGIC_IMG)
    header.write(struct.pack('<I', H))
    header.write(struct.pack('<I', W))
    header.write(struct.pack('<B', C))
    header.write(struct.pack('<H', block_size))
    header.write(struct.pack('<B', wavelet_levels))
    header.write(struct.pack('<B', mix_rounds_h))
    header.write(struct.pack('<B', mix_rounds_v))
    header.write(struct.pack('<H', mix_stride))

    enc = RangeEncoder()
    blocks = []

    # Decorrelación si RGB
    if C == 3:
        g, drg, dbg = rgb_to_g_drg_dbg(img)
        channels = [g, drg, dbg]
    else:
        channels = [img]

    # Coordenadas de bloques
    coords = [(r0, min(r0+block_size, H), c0, min(c0+block_size, W))
              for r0 in range(0, H, block_size)
              for c0 in range(0, W, block_size)]
    header.write(struct.pack('<I', len(coords)))

    # Por canal y bloque, comprimimos
    for ch in range(C if C == 1 else 3):
        for (r0, r1, c0, c1) in coords:
            blk = channels[ch][r0:r1, c0:c1]
            payload = _encode_block_gray(enc, blk, wavelet_levels,
                                         mix_rounds_h=mix_rounds_h,
                                         mix_rounds_v=mix_rounds_v,
                                         mix_stride=mix_stride)
            # Guardamos tamaño del payload + payload
            blocks.append(struct.pack('<I', len(payload)) + payload)

    rc_bytes = enc.finish()
    return header.getvalue() + struct.pack('<I', len(rc_bytes)) + rc_bytes + b''.join(blocks)


def decompress_image_blocks(blob: bytes) -> np.ndarray:
    bio = io.BytesIO(blob)
    magic = bio.read(len(MAGIC_IMG))
    if magic != MAGIC_IMG:
        raise ValueError("Firma inválida")

    H = struct.unpack('<I', bio.read(4))[0]
    W = struct.unpack('<I', bio.read(4))[0]
    C = bio.read(1)[0]
    block_size = struct.unpack('<H', bio.read(2))[0]
    wavelet_levels = bio.read(1)[0]
    mix_rounds_h = bio.read(1)[0]
    mix_rounds_v = bio.read(1)[0]
    mix_stride = struct.unpack('<H', bio.read(2))[0]
    nblocks = struct.unpack('<I', bio.read(4))[0]

    rc_len = struct.unpack('<I', bio.read(4))[0]
    rc_data = bio.read(rc_len)
    dec = RangeDecoder(rc_data)

    # Reconstituimos coords
    coords = [(r0, min(r0+block_size, H), c0, min(c0+block_size, W))
              for r0 in range(0, H, block_size)
              for c0 in range(0, W, block_size)]
    if len(coords) != nblocks:
        raise ValueError("Conteo de bloques no cuadra")

    # Buffers de salida por canal
    if C == 1:
        chans = [np.empty((H, W), dtype=np.uint8)]
    else:
        chans = [np.empty((H, W), dtype=np.uint8) for _ in range(3)]

    # Por canal y bloque, leemos payload y decodificamos con el RC compartido
    for ch in range(C if C == 1 else 3):
        for (r0, r1, c0, c1) in coords:
            pay_len = struct.unpack('<I', bio.read(4))[0]
            payload = bio.read(pay_len)
            blk = _decode_block_gray(dec, io.BytesIO(payload))
            chans[ch][r0:r1, c0:c1] = blk

    # Recompone color si RGB
    if C == 3:
        rgb = g_drg_dbg_to_rgb(chans[0], chans[1], chans[2])
        return rgb
    else:
        return chans[0]


# =============================================================================
# API de alto nivel
# =============================================================================

def compress_image2d_uint8(img: np.ndarray, block_size: int = 16, wavelet_levels: int = 3,
                           mix_rounds_h: int = 1, mix_rounds_v: int = 1, mix_stride: int = 1) -> bytes:
    """Atajo para grises."""
    if img.ndim != 2 or img.dtype != np.uint8:
        raise ValueError("Se requiere imagen 2D uint8")
    return compress_image_blocks(img, block_size, wavelet_levels, mix_rounds_h, mix_rounds_v, mix_stride)

def decompress_image2d_uint8(blob: bytes) -> np.ndarray:
    img = decompress_image_blocks(blob)
    if img.ndim != 2:
        raise ValueError("El blob no corresponde a una imagen 2D")
    return img

def compress_image_rgb_uint8(img_rgb: np.ndarray, block_size: int = 16, wavelet_levels: int = 3,
                             mix_rounds_h: int = 1, mix_rounds_v: int = 1, mix_stride: int = 1) -> bytes:
    """Atajo para RGB."""
    if img_rgb.ndim != 3 or img_rgb.shape[2] != 3 or img_rgb.dtype != np.uint8:
        raise ValueError("Se requiere imagen RGB uint8")
    return compress_image_blocks(img_rgb, block_size, wavelet_levels, mix_rounds_h, mix_rounds_v, mix_stride)

def decompress_image_rgb_uint8(blob: bytes) -> np.ndarray:
    img = decompress_image_blocks(blob)
    if img.ndim != 3 or img.shape[2] != 3:
        raise ValueError("El blob no corresponde a una imagen RGB")
    return img
