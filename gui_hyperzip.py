#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from pathlib import Path

from PyQt6 import QtWidgets, QtGui, QtCore
from PIL import Image
import numpy as np

import hyperzip as hz

APP_TITLE = "HyperZip GUI (PyQt6, lossless)"


def pil_to_np_uint8(img: Image.Image) -> np.ndarray:
    if img.mode == "RGB":
        return np.array(img, dtype=np.uint8)
    elif img.mode in ("L", "I;16", "I"):
        return np.array(img.convert("L"), dtype=np.uint8)
    else:
        return np.array(img.convert("RGB"), dtype=np.uint8)


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_TITLE)
        self.setMinimumSize(680, 460)

        lay = QtWidgets.QGridLayout(self)
        row = 0

        # Archivo fuente
        lay.addWidget(QtWidgets.QLabel("Archivo fuente:"), row, 0)
        self.in_edit = QtWidgets.QLineEdit()
        lay.addWidget(self.in_edit, row, 1)
        btn_in = QtWidgets.QPushButton("Explorar…")
        btn_in.clicked.connect(self.on_browse_in)
        lay.addWidget(btn_in, row, 2)
        row += 1

        # Archivo salida
        lay.addWidget(QtWidgets.QLabel("Archivo salida:"), row, 0)
        self.out_edit = QtWidgets.QLineEdit()
        lay.addWidget(self.out_edit, row, 1)
        btn_out = QtWidgets.QPushButton("Guardar como…")
        btn_out.clicked.connect(self.on_browse_out)
        lay.addWidget(btn_out, row, 2)
        row += 1

        # Parámetros
        params_group = QtWidgets.QGroupBox("Parámetros de compresión")
        params_lay = QtWidgets.QGridLayout(params_group)

        params_lay.addWidget(QtWidgets.QLabel("Tamaño de bloque:"), 0, 0)
        self.spin_block = QtWidgets.QSpinBox()
        self.spin_block.setRange(4, 256)
        self.spin_block.setValue(16)
        params_lay.addWidget(self.spin_block, 0, 1)

        params_lay.addWidget(QtWidgets.QLabel("Niveles wavelet:"), 1, 0)
        self.spin_levels = QtWidgets.QSpinBox()
        self.spin_levels.setRange(1, 8)
        self.spin_levels.setValue(3)
        params_lay.addWidget(self.spin_levels, 1, 1)

        params_lay.addWidget(QtWidgets.QLabel("Mix rounds H:"), 2, 0)
        self.spin_mix_h = QtWidgets.QSpinBox()
        self.spin_mix_h.setRange(0, 6)
        self.spin_mix_h.setValue(1)
        params_lay.addWidget(self.spin_mix_h, 2, 1)

        params_lay.addWidget(QtWidgets.QLabel("Mix rounds V:"), 3, 0)
        self.spin_mix_v = QtWidgets.QSpinBox()
        self.spin_mix_v.setRange(0, 6)
        self.spin_mix_v.setValue(1)
        params_lay.addWidget(self.spin_mix_v, 3, 1)

        params_lay.addWidget(QtWidgets.QLabel("Mix stride:"), 4, 0)
        self.spin_stride = QtWidgets.QSpinBox()
        self.spin_stride.setRange(1, 32)
        self.spin_stride.setValue(1)
        params_lay.addWidget(self.spin_stride, 4, 1)

        params_lay.addWidget(QtWidgets.QLabel("Modo:"), 5, 0)
        self.combo_mode = QtWidgets.QComboBox()
        self.combo_mode.addItems(["Detectar (auto)", "Forzar GRIS", "Forzar RGB"])
        self.combo_mode.setCurrentIndex(0)
        params_lay.addWidget(self.combo_mode, 5, 1)

        lay.addWidget(params_group, row, 0, 1, 3)
        row += 1

        # Acciones
        btns = QtWidgets.QHBoxLayout()
        self.btn_comp = QtWidgets.QPushButton("Comprimir")
        self.btn_comp.setDefault(True)
        self.btn_comp.clicked.connect(self.on_compress)
        btns.addWidget(self.btn_comp)

        self.btn_decomp = QtWidgets.QPushButton("Descomprimir")
        self.btn_decomp.clicked.connect(self.on_decompress)
        btns.addWidget(self.btn_decomp)

        lay.addLayout(btns, row, 0, 1, 3)
        row += 1

        # Log
        self.log = QtWidgets.QPlainTextEdit()
        self.log.setReadOnly(True)
        lay.addWidget(self.log, row, 0, 1, 3)

    # Helpers
    def log_info(self, msg):
        self.log.appendPlainText(msg)

    def error(self, message):
        QtWidgets.QMessageBox.critical(self, "Error", message)

    def info(self, title, message):
        QtWidgets.QMessageBox.information(self, title, message)

    # File pickers
    def on_browse_in(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Seleccionar archivo de entrada",
            "",
            "Imágenes (*.png *.jpg *.jpeg *.bmp *.tif *.tiff);;HyperZip (*.hzi);;Todos (*.*)"
        )
        if path:
            self.in_edit.setText(path)

    def on_browse_out(self):
        path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self,
            "Guardar como…",
            "",
            "HyperZip (*.hzi);;PNG (*.png);;Todos (*.*)"
        )
        if path:
            self.out_edit.setText(path)

    # Actions
    def on_compress(self):
        try:
            in_path = self.in_edit.text().strip()
            out_path = self.out_edit.text().strip()

            if not in_path:
                self.error("Selecciona una imagen de entrada.")
                return

            if not out_path:
                out_path = in_path + ".hzi"
                self.out_edit.setText(out_path)

            block = int(self.spin_block.value())
            levels = int(self.spin_levels.value())
            mix_h = int(self.spin_mix_h.value())
            mix_v = int(self.spin_mix_v.value())
            stride = int(self.spin_stride.value())

            ext = Path(in_path).suffix.lower()
            if ext not in [".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff"]:
                self.error("Para este GUI, usa imágenes (PNG/JPG/BMP/TIF).")
                return

            img = Image.open(in_path)
            npimg = pil_to_np_uint8(img)

            mode = self.combo_mode.currentIndex()
            if mode == 1:  # Forzar GRIS
                if npimg.ndim == 3:
                    npimg = npimg[..., 1]
            elif mode == 2:  # Forzar RGB
                if npimg.ndim != 3:
                    npimg = np.stack([npimg, npimg, npimg], axis=-1).astype(np.uint8)

            self.log_info("Comprimiendo…")
            blob = hz.compress_image_blocks(
                npimg,
                block_size=block,
                wavelet_levels=levels,
                mix_rounds_h=mix_h,
                mix_rounds_v=mix_v,
                mix_stride=stride,
            )
            with open(out_path, "wb") as f:
                f.write(blob)

            self.log_info(f"OK: Guardado en {out_path}")
            self.info("Completado", f"Archivo guardado:\n{out_path}")

        except Exception as e:
            self.error(f"Fallo al comprimir:\n{e}")

    def on_decompress(self):
        try:
            in_path = self.in_edit.text().strip()
            out_path = self.out_edit.text().strip()
            if not in_path:
                self.error("Selecciona un archivo .hzi de entrada.")
                return

            if not out_path:
                out_path = os.path.splitext(in_path)[0] + "_rec.png"
                self.out_edit.setText(out_path)

            self.log_info("Descomprimiendo…")
            blob = Path(in_path).read_bytes()
            img = hz.decompress_image_blocks(blob)

            # Guardar como PNG
            if img.ndim == 2:
                Image.fromarray(img, mode="L").save(out_path)
            else:
                Image.fromarray(img, mode="RGB").save(out_path)

            self.log_info(f"OK: Imagen reconstruida en {out_path}")
            self.info("Completado", f"Imagen reconstruida:\n{out_path}")

        except Exception as e:
            self.error(f"Fallo al descomprimir:\n{e}")


def main():
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
