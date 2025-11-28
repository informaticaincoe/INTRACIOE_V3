
(function(){
  // ======= Estado global POS =======
  window.POS = {
    items: [],   // {id, codigo, nombre, precio, cantidad, desc_pct, aplica_iva, stock}
    apiUrl: "{% url 'api_productos' %}",
  };

  // ======= Helpers / refs =======
  const $ = (id) => document.getElementById(id);
  const tbody       = $('tbody-items');
  const hiddenItems = $('hidden-items');
  const qtyInput    = $('cantidadProducto');
  const priceInput  = $('precioProducto');
  const ivaChk      = $('aplicaIvaProducto');

  const sumSub  = $('sum_subtotal');
  const sumIva  = $('sum_iva');
  const sumDesc = $('sum_desc');
  const sumTot  = $('sum_total');

  function fmt(n){ return '$' + (Number(n||0).toFixed(2)); }
  function escapeHtml(s){return String(s||'').replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]));}

  function lineTotal(it){
    const subtotal = (+it.precio) * it.cantidad;
    const desc = subtotal * (Math.min(100, Math.max(0, +it.desc_pct))/100);
    const base = subtotal - desc;
    const iva = it.aplica_iva ? base * 0.13 : 0;
    return base + iva;
  }

  // ======= Construye HIDDEN para el backend (siempre desde POS.items) =======
  function syncHidden(){
    hiddenItems.innerHTML = POS.items.map(it => `
      <input type="hidden" name="item_id[]" value="${it.id}">
      <input type="hidden" name="item_cantidad[]" value="${it.cantidad}">
      <input type="hidden" name="item_precio[]" value="${(+it.precio).toFixed(2)}">
      <input type="hidden" name="item_descuento[]" value="${it.desc_pct}">
      <input type="hidden" name="item_iva[]" value="${it.aplica_iva ? '1':'0'}">
      <input type="hidden" name="item_stock[]" value="${Number.isFinite(+it.stock)? it.stock : ''}">
    `).join('');
  }

  // ======= Render de filas =======
  function renderItems(){
    const items = POS.items;
    if (!items.length){
      tbody.innerHTML = `<tr class="empty"><td colspan="7" class="text-center text-muted py-3">Sin productos agregados.</td></tr>`;
      hiddenItems.innerHTML = '';
      return;
    }
    tbody.innerHTML = items.map((it, i) => {
      const stockTxt = Number.isFinite(+it.stock) ? it.stock : '-';
      const stockClass = (Number(it.stock) <= 0) ? 'stock-low' : 'stock-ok';
      return `
        <tr data-idx="${i}">
          <td>
            <div class="fw-semibold">${escapeHtml(it.nombre)}</div>
            <div class="small ${stockClass}">#${escapeHtml(it.codigo||'-')} · Stock: ${stockTxt}</div>
            <!-- ⚠️ OJO: aquí ya NO va hidden item_id[] -->
          </td>
          <td class="text-end">
            <input type="number" step="0.01" min="0" class="form-control form-control-sm text-end inp-precio" value="${(+it.precio).toFixed(2)}" aria-label="Precio unitario">
          </td>
          <td class="text-end">
            <input type="number" min="1" class="form-control form-control-sm text-end inp-cant" value="${it.cantidad}" aria-label="Cantidad">
          </td>
          <td class="text-end">
            <input type="number" min="0" max="100" class="form-control form-control-sm text-end inp-desc" value="${it.desc_pct}" aria-label="Descuento (%)">
          </td>
          <td class="text-center">
            <input class="form-check-input chk-iva" type="checkbox" ${it.aplica_iva ? 'checked':''} aria-label="Aplica IVA">
          </td>
          <td class="text-end cel-total">${fmt(lineTotal(it))}</td>
          <td class="text-end">
            <button type="button" class="btn btn-sm btn-outline-danger btn-del"><i class="bi bi-x-lg"></i></button>
          </td>
        </tr>
      `;
    }).join('');

    // listeners por fila
    tbody.querySelectorAll('tr').forEach(tr=>{
      const idx = +tr.dataset.idx;
      const item = POS.items[idx];
      tr.querySelector('.inp-precio').addEventListener('input', (e)=>{
        item.precio = parseFloat(e.target.value||'0')||0;
        tr.querySelector('.cel-total').textContent = fmt(lineTotal(item));
        calcTotals();
      });
      tr.querySelector('.inp-cant').addEventListener('input', (e)=>{
        item.cantidad = Math.max(1, parseInt(e.target.value||'1',10));
        tr.querySelector('.cel-total').textContent = fmt(lineTotal(item));
        calcTotals();
      });
      tr.querySelector('.inp-desc').addEventListener('input', (e)=>{
        let v = parseFloat(e.target.value||'0')||0; v = Math.max(0, Math.min(100, v));
        item.desc_pct = v;
        tr.querySelector('.cel-total').textContent = fmt(lineTotal(item));
        calcTotals();
      });
      tr.querySelector('.chk-iva').addEventListener('change', (e)=>{
        item.aplica_iva = e.target.checked;
        tr.querySelector('.cel-total').textContent = fmt(lineTotal(item));
        calcTotals();
      });
      tr.querySelector('.btn-del').addEventListener('click', ()=>{
        POS.items.splice(idx,1);
        renderItems();
        calcTotals();
      });
    });

    // HIDDEN al día
    syncHidden();
  }
  window.renderItems = renderItems;

  // ======= Totales =======
  function calcTotals(){
    let subtotal = 0, descuentos = 0, iva = 0, total = 0;
    POS.items.forEach(it=>{
      const st = (+it.precio) * it.cantidad;
      const ds = st * (Math.min(100, Math.max(0, +it.desc_pct))/100);
      const base = st - ds;
      const iv = it.aplica_iva ? base * 0.13 : 0;
      subtotal += base;
      descuentos += ds;
      iva += iv;
      total += base + iv;
    });

    const retIvaOn = $('ret_iva_sw')?.checked;
    const retRentaOn = $('ret_renta_sw')?.checked;
    let retIvaMto = retIvaOn ? parseFloat($('ret_iva_mto').value||'0')||0 : 0;
    let retRentaMto = retRentaOn ? parseFloat($('ret_renta_mto').value||'0')||0 : 0;

    sumSub.textContent  = fmt(subtotal);
    sumIva.textContent  = fmt(iva);
    sumDesc.textContent = fmt(descuentos);
    sumTot.textContent  = fmt(total - retIvaMto - retRentaMto);

    if ($('retencion_iva_monto'))   $('retencion_iva_monto').value   = retIvaMto.toFixed(2);
    if ($('retencion_renta_monto')) $('retencion_renta_monto').value = retRentaMto.toFixed(2);

    if (document.querySelector('input[name="metodo_pago"]:checked')?.value === 'EFECTIVO') {
      const recibido = parseFloat($('montoRecibido').value||'0')||0;
      const cambio = Math.max(0, recibido - (total - retIvaMto - retRentaMto));
      if ($('montoCambio')) $('montoCambio').textContent = fmt(cambio);
    }

    // HIDDEN al día
    syncHidden();
  }
  window.calcTotals = calcTotals;

  // Recalcular al cambiar retenciones / efectivo
  ;['ret_iva_sw','ret_iva_mto','ret_renta_sw','ret_renta_mto','montoRecibido'].forEach(id=>{
    $(id)?.addEventListener('input', calcTotals);
    $(id)?.addEventListener('change', calcTotals);
  });

  // ======= Add item (usado por el picker) =======
  function addItemFromProduct(sel){
    if(!sel) return;
    const cant   = Math.max(1, parseInt(qtyInput.value||'1',10));
    const aplica = ivaChk.checked;
    const precio = parseFloat(priceInput.value || sel.precio || '0') || 0;

    const idx = POS.items.findIndex(x => x.id === sel.id);
    if (idx >= 0) {
      POS.items[idx].cantidad += cant;
      if (!priceInput.value) POS.items[idx].precio = +sel.precio; // mantener neto base si no se forzó
    } else {
      POS.items.push({
        id: sel.id,
        codigo: sel.codigo,
        nombre: sel.nombre,
        precio: precio,
        cantidad: cant,
        desc_pct: 0,
        aplica_iva: aplica,
        stock: sel.stock
      });
    }

    qtyInput.value = 1;
    renderItems();
    calcTotals();
  }
  window.addItem = () => {}; // placeholder, el picker lo invoca con su selección

  // ======= Picker =======
  class ProductPicker {
    constructor({input, menu, apiUrl, onChoose}){
      this.input = input;
      this.menu  = menu;
      this.apiUrl = apiUrl;
      this.onChoose = onChoose || (()=>{});
      this.items = [];
      this.activeIndex = -1;
      this.selected = null;

      this.input.addEventListener('focus', ()=> this.search(''));
      this.input.addEventListener('input',  (e)=> this.debouncedSearch(e.target.value.trim()));
      this.input.addEventListener('keydown',(e)=> this.onKey(e));
      document.addEventListener('click', (e)=>{
        if(!this.menu.contains(e.target) && e.target!==this.input){ this.hide(); }
      });
    }
    debouncedSearch(q){ clearTimeout(this._t); this._t = setTimeout(()=>this.search(q), 180); }
    async search(q){
      try{
        const url = `${this.apiUrl}?q=${encodeURIComponent(q)}&page_size=25`;
        const res = await fetch(url, {headers:{'X-Requested-With':'XMLHttpRequest'}});
        const data = await res.json();
        this.items = (data.results||[]).map(p=>{
          const precio = parseFloat(p.precio||'0')||0;
          const neto = p.con_iva ? (precio/1.13) : precio; // trabajar en neto
          return { id:p.id, codigo:p.codigo, nombre:p.nombre, precio:neto,
                   con_iva: !!p.con_iva, stock: p.stock, imagen:p.imagen||'' };
        });
        this.activeIndex = this.items.length ? 0 : -1;
        this.render(); this.show();
      }catch(_e){ this.items=[]; this.activeIndex=-1; this.render(); this.show(); }
    }
    render(){
      if(!this.items.length){ this.menu.innerHTML = `<div class="combo-empty p-2 text-muted">Sin resultados…</div>`; return; }
      this.menu.innerHTML = this.items.map((it,i)=>`
        <div class="combo-item ${i===this.activeIndex?'active':''} p-2" role="option" data-idx="${i}" style="cursor:pointer;">
          <div class="d-flex align-items-center justify-content-between gap-3">
            <div class="me-3">
              <div class="fw-semibold">${this.escape(it.nombre)}</div>
              <div class="small ${(+it.stock)<=0?'text-danger':'text-success'}">
                #${this.escape(it.codigo||'-')} · Stock: ${Number.isFinite(+it.stock)?it.stock:'-'}
              </div>
            </div>
            <div class="ms-auto text-nowrap">
              <span class="badge text-bg-light">$${(+it.precio).toFixed(2)}</span>
            </div>
          </div>
        </div>
      `).join('');
      this.menu.querySelectorAll('.combo-item').forEach(el=>{
        el.addEventListener('click', ()=>{
          const idx = +el.dataset.idx; this.choose(idx);
        });
      });
    }
    onKey(e){
      if(!this.isOpen()) this.show();
      if(e.key==='ArrowDown'){ e.preventDefault(); this.move(1); }
      else if(e.key==='ArrowUp'){ e.preventDefault(); this.move(-1); }
      else if(e.key==='Enter'){ e.preventDefault(); this.choose(this.activeIndex); }
      else if(e.key==='Escape'){ this.hide(); }
    }
    move(delta){
      if(!this.items.length) return;
      this.activeIndex = (this.activeIndex + delta + this.items.length) % this.items.length;
      this.render();
      this.menu.querySelector('.combo-item.active')?.scrollIntoView({block:'nearest'});
    }
    choose(idx){
      const item = this.items[idx]; if(!item) return;
      this.selected = item;
      this.input.value = `${item.codigo} | ${item.nombre}`;
      this.onChoose(item);
      this.hide();
    }
    getSelected(){ return this.selected; }
    focus(){ this.input.focus(); }
    isOpen(){ return this.menu.style.display!=='none'; }
    show(){ this.menu.style.display='block'; }
    hide(){ this.menu.style.display='none'; }
    escape(s){return String(s||'').replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]));}
  }

  // Instancia del picker
  const picker = new ProductPicker({
    input: $('productoPickerInput'),
    menu:  $('productoPickerMenu'),
    apiUrl: POS.apiUrl,
    onChoose: (prod)=>{
      // precargar precio neto y ajustar IVA por defecto
      priceInput.value = (+prod.precio).toFixed(2);
      priceInput.dataset.sticky = '1'; // no se borra tras agregar
      ivaChk.checked = !prod.con_iva;  // si venía con IVA incluido, apagamos IVA de línea
      // al Enter del input, si ya se eligió, agregamos
      setTimeout(()=>{ addItemFromProduct(prod); }, 10);
    }
  });
  window.PRODUCT_PICKER = picker;

  // Enter en el input → si hay seleccionado, agregar
  $('productoPickerInput').addEventListener('keydown', (e)=>{
    if(e.key==='Enter'){
      const sel = picker.getSelected();
      if(sel){ e.preventDefault(); addItemFromProduct(sel); }
    }
  });

  // Botón Agregar
  $('btnAgregarProducto')?.addEventListener('click', ()=>{
    const sel = picker.getSelected();
    if(!sel){ picker.focus(); return; }
    addItemFromProduct(sel);
  });

  // Método de pago toggles
  function togglePago(){
    const mp = document.querySelector('input[name="metodo_pago"]:checked')?.value;
    $('wrap-efectivo') && ($('wrap-efectivo').style.display = (mp === 'EFECTIVO') ? '' : 'none');
    $('wrap-credito')  && ($('wrap-credito').style.display  = (mp === 'CREDITO')  ? '' : 'none');
    calcTotals();
  }
  document.querySelectorAll('input[name="metodo_pago"]').forEach(r => r.addEventListener('change', togglePago));
  togglePago();

  // ======= Submit: usar fetch para recibir JSON y redirigir =======
  const form = document.getElementById('form-pos');
  form.addEventListener('submit', async (e) => {
    if (POS.items.length === 0) {
      e.preventDefault();
      alert('Agrega al menos un producto.');
      picker.focus();
      return;
    }

    e.preventDefault();
    // Asegura que los hidden reflejen lo que hay en pantalla
    if (typeof window.calcTotals === 'function') window.calcTotals();

    try {
      const fd = new FormData(form);
      const resp = await fetch(form.action || location.href, {
        method: 'POST',
        body: fd,
        headers: { 'X-Requested-With':'XMLHttpRequest' }
      });
      const data = await resp.json();
      if (!resp.ok) { alert(data?.error || 'Error al generar la factura.'); return; }
      if (data.redirect) { window.location.href = data.redirect; return; }
      alert(data?.mensaje || 'Operación completada.');
    } catch (err) {
      console.error('Submit error:', err);
      form.submit(); // Fallback
    }
  });

  // Atajo F9 para enviar
  document.addEventListener('keydown', (e)=>{
    if (e.key === 'F9') { e.preventDefault(); form.requestSubmit(); }
  });

  // Si el usuario edita a mano el precio base, marcamos "sticky"
  priceInput.addEventListener('input', ()=> priceInput.dataset.sticky = priceInput.value ? '1' : '');

})();

