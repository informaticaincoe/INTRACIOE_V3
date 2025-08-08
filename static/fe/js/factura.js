// ===== Helpers =====
const $ = (sel, ctx=document)=> ctx.querySelector(sel);
const $$ = (sel, ctx=document)=> Array.from(ctx.querySelectorAll(sel));
const asNumber = (v, d=0)=> {
  const n = Number(String(v ?? '').toString().replace(',', '.'));
  return Number.isFinite(n) ? n : d;
};
function roundHalfUp(value, decimals){ const m=Math.pow(10, decimals); return Math.round(value * m) / m; }
function showEl(el){ if(el) el.hidden = false; }
function hideEl(el){ if(el) el.hidden = true; }
function setEmptyStateTbody(tbody, isEmpty, cols){
  const existing = tbody.querySelector('.empty-row');
  if(isEmpty){
    if(!existing){
      const tr = document.createElement('tr');
      tr.className='empty-row';
      tr.innerHTML = `<td colspan="${cols}" class="empty-state">No hay registros.</td>`;
      tbody.appendChild(tr);
    }
  } else {
    existing && existing.remove();
  }
}
function toast(msg){ alert(msg); } // Puedes migrar a Toast de Bootstrap si quieres

// ===== Global state =====
let facturasRelacionadas = [];
let descuento_sel_item = 0;
let totalCompletado = false;

// ===== Stepper =====
function goToStep(step){
  // secciones
  $$('.form-section').forEach(sec => {
    if(sec.dataset.step === String(step)) showEl(sec); else hideEl(sec);
  });
  // stepper visual
  $$('.stepper li').forEach(li=>{
    li.classList.toggle('active', li.dataset.step === String(step));
  });
}
function bindStepper(){
  $$('.btn-next').forEach(btn=>{
    btn.addEventListener('click', ()=>{
      const next = btn.dataset.next;
      if(next) goToStep(next);
    });
  });
  $$('.btn-prev').forEach(btn=>{
    btn.addEventListener('click', ()=>{
      const prev = btn.dataset.prev;
      if(prev) goToStep(prev);
    });
  });
  goToStep(1);
}

// ===== Init bindings =====
document.addEventListener('DOMContentLoaded', () => {
  bindStepper();
  bindCore();
  bindProductosModal();
  bindDocFisicoModal();
  bindFormasPagoModal();
  bindRetenciones();
  actualizarProductos(); // primer fetch
  actualizarResumen();   // primer cálculo
  // Tooltips
  const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
  tooltipTriggerList.map(el => new bootstrap.Tooltip(el));
});

// ===== Core bindings =====
function bindCore(){
  // Receptor: mostrar formulario para "nuevo"
  $('#receptor-select').addEventListener('change', (e)=>{
    if(e.target.value === 'nuevo') showEl($('#nuevo-receptor')); else hideEl($('#nuevo-receptor'));
  });

  // Tipo DTE → actualiza número control + productos
  const td = $('#tipo_documento_select');
  td.addEventListener('change', async ()=>{
    try{
      const res = await fetch(`/fe/obtener-numero-control/?tipo_dte=${td.value}`);
      const data = await res.json();
      $('#numero_control_input').value = data.numero_control || '';
    }catch(err){ console.error('obtener-numero-control', err); }
    await actualizarProductos();
    actualizarResumen();
  });

  // Documento relacionado tipo
  $('#documento_select').addEventListener('change', (e)=>{
    const v = e.target.value;
    if(v === '2'){ // electrónico
      showEl($('#div-electronic')); hideEl($('#div-physical')); showEl($('#btn_add_relacion'));
    } else if(v === '1'){ // físico
      hideEl($('#div-electronic')); showEl($('#div-physical')); hideEl($('#btn_add_relacion'));
      abrirModalDocFisico();
    } else {
      hideEl($('#div-electronic')); hideEl($('#div-physical')); hideEl($('#btn_add_relacion'));
    }
  });

  // Agregar doc relacionado electrónico
  $('#btn_add_relacion').addEventListener('click', cargarFacturaRelacionada);

  // Descuentos globales recalculan
  $('#descuento-global').addEventListener('input', actualizarResumen);
  $('#descuento_gravado').addEventListener('input', actualizarResumen);

  // Form submit
  $('#form-factura').addEventListener('submit', validacionesFormulario);
}

// ===== Productos (modal) =====
function bindProductosModal(){
  // Cambios de descuento por ítem en modal
  document.addEventListener('change', (e)=>{
    if(e.target.classList.contains('descuento-select')){
      descuento_sel_item = asNumber(e.target.value, 0);
    }
  });
  // Cargar al confirmar modal
  $('#btn-cargar-productos').addEventListener('click', cargarProductosModal);
}

async function actualizarProductos(){
  const tipo_dte = $('#tipo_documento_select').value;
  const tbody = $('#tabla-productos-modal tbody');
  const table = $('#tabla-productos-modal');
  const urlBase = table?.dataset?.url;  // <- viene del HTML

  if(!urlBase){
    console.error('Falta data-url en #tabla-productos-modal');
    tbody.innerHTML = `<tr><td colspan="7" class="empty-state">No se configuró la URL de productos.</td></tr>`;
    return;
  }

  tbody.innerHTML = `<tr><td colspan="7" class="empty-state">Cargando productos…</td></tr>`;

  try{
    const url = `${urlBase}?tipo_documento_dte=${encodeURIComponent(tipo_dte)}`;
    const res = await fetch(url, { headers:{'X-Requested-With':'XMLHttpRequest'} });
    if(!res.ok) throw new Error('Error al obtener productos');

    // Si tu endpoint devuelve HTML de fragmento
    const html = await res.text();
    const frag = new DOMParser().parseFromString(html, 'text/html');
    const newTbody = frag.querySelector('#tabla-productos-modal tbody') || frag.querySelector('tbody');
    if(!newTbody) throw new Error('La respuesta no contiene <tbody>');

    tbody.innerHTML = newTbody.innerHTML;
  }catch(e){
    console.error('Productos error:', e);
    tbody.innerHTML = `<tr><td colspan="7" class="empty-state">No se pudieron cargar los productos.</td></tr>`;
  }
}

function cargarProductosModal(){
  const rows = $$('#tabla-productos-modal tbody tr');
  rows.forEach(row=>{
    const checkbox = row.querySelector('.producto-checkbox');
    if(checkbox && checkbox.checked){
      const productoId   = row.getAttribute('data-id');
      const productoText = row.cells[1].textContent.trim();
      const precio_incl  = roundHalfUp(row.querySelector('.precio-unitario').getAttribute('data-precio').replace(',', '.'), 6);
      const cantidad     = row.querySelector('.cantidad-input').value;
      const aplica_iva   = row.querySelector('.producto-con-iva').getAttribute('data-prod-iva');
      agregarProductoFilaTabla(productoId, productoText, precio_incl, cantidad, aplica_iva);
    }
  });
  actualizarResumen();
  closeModal('productosModal');
}

function agregarProductoFilaTabla(productoId, productoText, precio_incl, cantidad, aplica_iva){
  const tipo_dte = $('#tipo_documento_select').value;

  let neto_unitario=0, iva_unitario=0, qty=0, total_neto=0, total_iva=0, total_incl=0, monto_descuento=0;
  let porcentaje_descu = roundHalfUp((asNumber(descuento_sel_item,0)/100), 6);

  qty = parseFloat(cantidad);
  neto_unitario = roundHalfUp(precio_incl, 6);

  if(tipo_dte == "01"){
    iva_unitario = roundHalfUp(((neto_unitario / 1.13) * 0.13), 6);
    total_neto = roundHalfUp((neto_unitario * qty), 6);
    monto_descuento = roundHalfUp((total_neto * porcentaje_descu), 6);
    total_incl = roundHalfUp((total_neto - roundHalfUp(monto_descuento, 2)), 6);
    total_iva  = roundHalfUp(((total_incl / 1.13) * 0.13), 6);
  }else{
    iva_unitario = roundHalfUp((neto_unitario * 0.13), 6);
    total_neto   = roundHalfUp((neto_unitario * qty), 6);
    monto_descuento = roundHalfUp((total_neto * porcentaje_descu), 6);
    const pre_unitario_iva = roundHalfUp(total_neto, 6);
    total_incl = roundHalfUp((pre_unitario_iva - roundHalfUp(monto_descuento, 2)), 6);
    total_iva  = roundHalfUp((total_incl * 0.13), 6);
  }

  const tbody = $('#tbody-productos');

  // Merge por ID
  let existe = false;
  $$('#tbody-productos tr').forEach(row=>{
    if(row.getAttribute('data-id') === productoId){
      const inputCantidad = row.querySelector('.cantidad-input');
      inputCantidad.value = (asNumber(inputCantidad.value,1) + qty);
      actualizarFila(inputCantidad);
      existe = true;
    }
  });
  if(existe){ setEmptyStateTbody(tbody, false, 10); return; }

  const tr = document.createElement('tr');
  tr.setAttribute('data-id', productoId);
  tr.innerHTML = `
    <td class="text-start">${productoText}</td>
    <td class="precio-neto" data-precio-neto="${neto_unitario}">${parseFloat(neto_unitario).toFixed(2)}</td>
    <td class="iva-unitario" data-iva-unitario="${iva_unitario}">${parseFloat(iva_unitario).toFixed(2)}</td>
    <td><input type="number" class="cantidad-input form-control" value="${qty}" min="1" style="width:100px"></td>
    <td class="total-neto" data-total-neto="${total_neto}">${parseFloat(total_neto).toFixed(2)}</td>
    <td class="descuento-item">${parseFloat(porcentaje_descu * 100)}%</td>
    <td class="total-incl" data-total-incl="${total_incl}">${parseFloat(total_incl).toFixed(2)}</td>
    <td class="total-iva">${parseFloat(total_iva).toFixed(2)}</td>
    <td class="aplica-iva">${aplica_iva}</td>
    <td><button type="button" class="btn btn-danger btn-sm btn-del-item">Eliminar</button></td>
  `;
  tbody.appendChild(tr);
  setEmptyStateTbody(tbody, false, 10);

  // bind dinámico
  tr.querySelector('.cantidad-input').addEventListener('input', e=> actualizarFila(e.target));
  tr.querySelector('.btn-del-item').addEventListener('click', ()=>{
    if(confirm('¿Eliminar este producto?')){
      tr.remove();
      setEmptyStateTbody(tbody, tbody.querySelectorAll('tr').length===0, 10);
      actualizarResumen();
    }
  });

  descuento_sel_item = 0;
}

function actualizarFila(input){
  const tipo_dte = $('#tipo_documento_select').value;
  const row = input.closest('tr');
  const precio_neto = roundHalfUp(row.querySelector('.precio-neto').getAttribute('data-precio-neto'), 6);
  const iva_unitario= roundHalfUp(row.querySelector('.iva-unitario').getAttribute('data-iva-unitario'), 6);
  const cantidad    = parseFloat(input.value) || 0;
  const total_neto  = roundHalfUp((precio_neto*cantidad), 6);
  const descuento_item = asNumber((row.querySelector('.descuento-item').textContent).replace('%',''),0)/100;
  const monto_descuento_item = roundHalfUp((total_neto * descuento_item), 6);

  let total_incl = roundHalfUp((total_neto - roundHalfUp(monto_descuento_item, 2)), 6);
  let total_iva = 0;

  if(tipo_dte=="01"){
    total_iva = roundHalfUp(((total_incl/1.13)*0.13),6);
  }else{
    total_iva = roundHalfUp((total_incl*0.13),6);
  }

  row.querySelector('.total-neto').textContent = roundHalfUp(total_neto,2).toFixed(2);
  row.querySelector('.total-iva').textContent  = parseFloat(total_iva).toFixed(2);
  row.querySelector('.total-incl').textContent = parseFloat(total_incl).toFixed(2);
  actualizarResumen();
}

// ===== Resumen =====
function actualizarResumen(){
  const tipo_dte = $('#tipo_documento_select').value;

  let sumNeto=0, sumIVA=0, sumIncl=0, sumMontoDescu=0, sumIncIva=0;
  let valorTributo=0, montoTotalOperacion=0;

  // Productos
  $$('#tabla-productos tbody tr:not(.empty-row)').forEach(row=>{
    const netoCell = row.querySelector('.total-neto');
    if(netoCell){
      sumNeto += asNumber(netoCell.textContent, 0);
      sumIVA  += asNumber(row.querySelector('.total-iva').textContent, 0);
      sumIncl += asNumber(row.querySelector('.total-incl').textContent, 0);
      sumIncIva += asNumber(row.querySelector('.total-incl').getAttribute('data-total-incl'), 0);

      const montoNeto = asNumber(netoCell.textContent, 0);
      const porcentajeDescu = (asNumber(row.querySelector('.descuento-item').textContent.replace('%',''),0)/100);
      const montoDescu = roundHalfUp((montoNeto * porcentajeDescu), 6);
      sumMontoDescu += roundHalfUp(montoDescu, 2);
    }
  });

  // Facturas relacionadas
  $$('#facturasAccordion .accordion-body table tbody tr').forEach(row=>{
    const netoCell = row.querySelector('.total-neto');
    if(netoCell){
      sumNeto += asNumber(netoCell.textContent, 0);
      sumIVA  += asNumber(row.querySelector('.total-iva').textContent, 0);
      sumIncl += asNumber(row.querySelector('.total-incl').textContent, 0);
      sumIncIva += asNumber(row.querySelector('.total-incl').getAttribute('data-total-incl'), 0);

      const montoNeto = asNumber(netoCell.textContent, 0);
      const porcentajeDescu = (asNumber(row.querySelector('.descuento-item')?.textContent?.replace('%','') || 0,0)/100);
      const montoDescu = roundHalfUp((montoNeto * porcentajeDescu), 6);
      sumMontoDescu += roundHalfUp(montoDescu, 2);
    }
  });

  $('#subtotal-neto').textContent = roundHalfUp(sumNeto,2).toFixed(2);
  $('#total-iva').textContent     = roundHalfUp(sumIVA,2).toFixed(2);
  $('#total-incl').textContent    = roundHalfUp(sumIncl,2).toFixed(2);

  const monto_porc_gravado = asNumber($('#descuento_gravado').value,0)/100;
  const descu_gravado = roundHalfUp((sumIncl * monto_porc_gravado), 6);
  const suma_descuentos = roundHalfUp((sumMontoDescu + descu_gravado), 6);

  const descuentoPorc         = asNumber($('#descuento-global').value,0);
  const montoDescuentoGlobal  = roundHalfUp((sumIncl * descuentoPorc / 100), 2);
  const descuentoPorcGravado  = asNumber($('#descuento_gravado').value,0);
  const montoDescuGravado     = roundHalfUp((sumIncl * descuentoPorcGravado / 100), 2);
  const subTotal              = roundHalfUp((sumIncl - montoDescuGravado - montoDescuentoGlobal), 2);

  if(tipo_dte!="01"){
    valorTributo = roundHalfUp(sumIVA, 2);
    montoTotalOperacion = roundHalfUp((subTotal + valorTributo), 2);
  }else{
    montoTotalOperacion = subTotal;
  }
  const totalPagar = montoTotalOperacion;

  $('#monto_descuento').textContent   = suma_descuentos.toFixed(2);
  $('#total-pagar').textContent       = totalPagar.toFixed(2);
  $('#total-pagar-fp').textContent    = totalPagar.toFixed(2);
  $('#sub-total-resumen').textContent = subTotal.toFixed(2);
  $('#monto_tributo').textContent     = valorTributo.toFixed(2);
  $('#total-operacion').textContent   = montoTotalOperacion.toFixed(2);
}

// ===== Formas de pago =====
function bindFormasPagoModal(){
  $('#btn-aceptar-fp').addEventListener('click', ()=>{
    cargarFormasPagoModal();
  });
}
function cargarFormasPagoModal(){
  const condicion_operacion = $('#condicion_op').value;
  const saldo_favor = $('#saldo_favor_input').value;
  const total_pagar = asNumber($('#total-pagar').textContent, 0);
  const rows = $$('#tabla-formaspago-modal tbody tr');

  let recibido_fp = 0;

  rows.forEach(row=>{
    const checkbox = row.querySelector('.formapago-checkbox');
    if(checkbox.checked){
      const fpId = row.getAttribute('data-id');
      const num_referencia_fp = row.querySelector('.referencia-input').value;
      const monto_fp = asNumber(row.querySelector('.monto-input').value, 0);
      const periodo_plazo = asNumber(row.querySelector('.periodo-input').value, 0);

      const hipotetico = recibido_fp + monto_fp;
      if(hipotetico > total_pagar){
        checkbox.checked = false;
        toast("El monto total ya ha sido alcanzado.");
        totalCompletado = true;
        return;
      }

      recibido_fp += monto_fp;
      $('#recibido').textContent = recibido_fp.toFixed(2);

      fetch(`/fe/obtener-forma-pago/?fp_id=${fpId}&num_ref=${encodeURIComponent(num_referencia_fp)}&monto_fp=${monto_fp}&periodo=${periodo_plazo}&saldo_favor_r=${encodeURIComponent(saldo_favor)}&condicion_op=${encodeURIComponent(condicion_operacion)}&total_pagar=${total_pagar}`)
        .then(r=>{ if(!r.ok) throw new Error('Network response not ok'); return r.json(); })
        .catch(err=> console.error('FP error:', err));
    }
  });
  closeModal('formasPagoModal');
}

// ===== Documento relacionado =====
function cargarFacturaRelacionada(){
  const codigoGeneracion = ($('#documento_relacionado_input')?.value || '').trim();
  if(!codigoGeneracion){ toast("Ingresa el código de generación."); return; }

  fetch(`/fe/documento-relacionado/?codigo_generacion=${encodeURIComponent(codigoGeneracion)}`)
    .then(r=>r.json())
    .then(data=>{
      if(data.error){ toast(data.error); return; }
      agregarFacturaAccordion(data);
    })
    .catch(err=>{ console.error('Relación error:', err); toast("Error al obtener la factura."); });
}

function agregarFacturaAccordion(factura){
  const facturaId = factura.codigo_generacion;
  const accordion = $('#facturasAccordion');
  const empty = accordion.querySelector('.empty-state'); if(empty) empty.remove();

  const item = document.createElement('div');
  item.className = 'accordion-item';
  item.setAttribute('data-factura-id', facturaId);

  item.innerHTML = `
    <h2 class="accordion-header" id="heading-${facturaId}">
      <div class="d-flex justify-content-between align-items-center w-100">
        <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapse-${facturaId}" aria-expanded="false" aria-controls="collapse-${facturaId}">
          Factura: ${factura.codigo_generacion} | Fecha: ${factura.fecha_emision} | Total: ${factura.total}
        </button>
        <button type="button" class="btn btn-danger btn-sm ms-2 btn-del-fact">Eliminar</button>
      </div>
    </h2>
    <div id="collapse-${facturaId}" class="accordion-collapse collapse" aria-labelledby="heading-${facturaId}" data-bs-parent="#facturasAccordion">
      <div class="accordion-body">
        ${crearTablaDetalles(factura.detalles)}
      </div>
    </div>
  `;
  accordion.appendChild(item);

  // eventos
  item.querySelector('.btn-del-fact').addEventListener('click', ()=>{
    if(confirm('¿Eliminar la factura relacionada?')){
      item.remove();
      facturasRelacionadas = facturasRelacionadas.filter(f=> f.codigo_generacion !== facturaId);
      if(!accordion.querySelector('.accordion-item')){
        const div = document.createElement('div');
        div.className='empty-state'; div.textContent='No hay documentos relacionados.';
        accordion.appendChild(div);
      }
      actualizarResumen();
    }
  });

  facturasRelacionadas.push(factura);
  actualizarResumen();
}

function crearTablaDetalles(detalles){
  const list = (detalles || []).filter(d=> !(d.producto||'').toUpperCase().includes('TOTAL'));
  let html = `
    <table class="table table-bordered">
      <thead>
        <tr>
          <th>Producto</th>
          <th>P. Unit. (Neto)</th>
          <th>IVA Unit.</th>
          <th>Cantidad</th>
          <th>Total Neto</th>
          <th>Total IVA</th>
          <th>Total con IVA</th>
          <th>Descuento</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
  `;
  list.forEach(prod=>{
    const precioIncl = asNumber(prod.precio_unitario, 0);
    const neto = precioIncl / 1.13;
    const iva  = precioIncl - neto;
    const cantidad = asNumber(prod.cantidad, 0);
    const totalNeto = neto * cantidad;
    const totalIVA  = iva * cantidad;
    const totalIncl = precioIncl * cantidad;

    html += `
      <tr data-id="${prod.id}">
        <td class="text-start">${prod.producto}</td>
        <td>${neto.toFixed(2)}</td>
        <td>${iva.toFixed(2)}</td>
        <td><input type="number" class="form-control form-control-sm cantidad-input-invoice" value="${cantidad}" min="1"></td>
        <td class="total-neto">${totalNeto.toFixed(2)}</td>
        <td class="total-iva">${totalIVA.toFixed(2)}</td>
        <td class="total-incl" data-total-incl="${totalIncl.toFixed(2)}">${totalIncl.toFixed(2)}</td>
        <td class="descuento-item">${prod.descuento || ''}</td>
        <td><button type="button" class="btn btn-danger btn-sm btn-del-inv">Eliminar</button></td>
      </tr>
    `;
  });
  html += `</tbody></table>`;
  return html;
}

// Delegación para filas de facturas relacionadas
document.addEventListener('input', (e)=>{
  if(e.target.classList.contains('cantidad-input-invoice')){
    const row = e.target.closest('tr');
    const precioUnitario = asNumber(row.cells[1].textContent,0);
    const ivaUnitario = asNumber(row.cells[2].textContent,0);
    const cantidad = asNumber(e.target.value,0);
    const totalNeto = precioUnitario * cantidad;
    const totalIVA  = ivaUnitario * cantidad;
    const totalIncl = (precioUnitario + ivaUnitario) * cantidad;
    row.querySelector('.total-neto').textContent = totalNeto.toFixed(2);
    row.querySelector('.total-iva').textContent  = totalIVA.toFixed(2);
    row.querySelector('.total-incl').textContent = totalIncl.toFixed(2);
    row.querySelector('.total-incl').setAttribute('data-total-incl', totalIncl.toFixed(2));
    actualizarResumen();
  }
});
document.addEventListener('click', (e)=>{
  if(e.target.classList.contains('btn-del-inv')){
    const row = e.target.closest('tr');
    if(confirm('¿Eliminar este producto de la factura relacionada?')){
      row.remove();
      actualizarResumen();
    }
  }
});

// ===== Documento físico =====
function bindDocFisicoModal(){
  $('#btn-doc-fisico').addEventListener('click', abrirModalDocFisico);
  $('#btn-guardar-doc-fisico').addEventListener('click', guardarDocFisico);
}
function abrirModalDocFisico(){ openModal('modalDocFisico'); }
function guardarDocFisico(){
  const doc = {
    numero_control: $('#fisico-numero-control').value,
    codigo_generacion: $('#fisico-codigo-generacion').value,
    fecha: $('#fisico-fecha').value,
    hora: $('#fisico-hora').value,
    total: "0.00",
    detalles: []
  };
  agregarFacturaAccordionFisica(doc);
  closeModal('modalDocFisico');
}
function agregarFacturaAccordionFisica(doc){
  const docId = doc.codigo_generacion || (crypto?.randomUUID?.() || String(Date.now()));
  const accordion = $('#facturasAccordion');
  const empty = accordion.querySelector('.empty-state'); if(empty) empty.remove();

  const item = document.createElement('div');
  item.className='accordion-item';
  item.setAttribute('data-factura-id', docId);
  item.innerHTML = `
    <h2 class="accordion-header" id="heading-${docId}">
      <div class="d-flex justify-content-between align-items-center w-100">
        <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapse-${docId}" aria-expanded="false" aria-controls="collapse-${docId}">
          Documento Físico: ${doc.codigo_generacion || 'N/A'} | Fecha: ${doc.fecha || '—'} | Total: ${doc.total}
        </button>
        <button type="button" class="btn btn-danger btn-sm ms-2 btn-del-fact">Eliminar</button>
      </div>
    </h2>
    <div id="collapse-${docId}" class="accordion-collapse collapse" aria-labelledby="heading-${docId}" data-bs-parent="#facturasAccordion">
      <div class="accordion-body">
        ${crearTablaDetalles(doc.detalles || [])}
      </div>
    </div>
  `;
  accordion.appendChild(item);
  item.querySelector('.btn-del-fact').addEventListener('click', ()=>{
    if(confirm('¿Eliminar la factura relacionada?')){
      item.remove();
      facturasRelacionadas = facturasRelacionadas.filter(f=> f.codigo_generacion !== docId);
      if(!accordion.querySelector('.accordion-item')){
        const div = document.createElement('div');
        div.className='empty-state'; div.textContent='No hay documentos relacionados.';
        accordion.appendChild(div);
      }
      actualizarResumen();
    }
  });
  facturasRelacionadas.push(doc);
  actualizarResumen();
}

// ===== Retenciones =====
function bindRetenciones(){
  $('#retencion_iva_checkbox').addEventListener('change', e=>{
    $('#btn-retencion-iva').style.display = e.target.checked ? 'inline-block' : 'none';
  });
  $('#retencion_renta_checkbox').addEventListener('change', e=>{
    $('#btn-retencion-renta').style.display = e.target.checked ? 'inline-block' : 'none';
  });
  $('#btn-guardar-ret-iva')?.addEventListener('click', ()=> closeModal('retencionIvaModal'));
  $('#btn-guardar-ret-renta')?.addEventListener('click', ()=> closeModal('retencionRentaModal'));
}

// ===== Modals helpers =====
function openModal(id){
  const el = document.getElementById(id);
  new bootstrap.Modal(el).show();
}
function closeModal(id){
  const el = document.getElementById(id);
  const inst = bootstrap.Modal.getInstance(el);
  if(inst) inst.hide();
}

// ===== Submit & Validaciones =====
function validacionesFormulario(e){
  e.preventDefault();

  const tipo_dte  = $('#tipo_documento_select').value;
  const receptor  = $('#receptor-select').value;
  const total     = asNumber($('#total-pagar').textContent, 0);
  const recibido  = asNumber($('#recibido').textContent, 0);
  const nombreResp= ($('#nombre_responsable').value || '').trim();
  const docResp   = ($('#documento_responsable').value || '').trim();

  const errors = [];
  if(!receptor) errors.push('Seleccione un receptor.');
  if($$('#tbody-productos tr:not(.empty-row)').length === 0) errors.push('Debe agregar al menos un producto.');
  if(total <= 0) errors.push('El total a pagar debe ser mayor a 0.');
  if(recibido < total) errors.push('Agregue formas de pago suficientes para cubrir el total.');
  if(tipo_dte === '03' && total >= 25000 && (!nombreResp || !docResp)) errors.push('Para Notas de Crédito ≥ $25,000 debe indicar Responsable y Documento.');

  const box = $('#form-errors');
  if(errors.length){
    box.style.display = 'block';
    box.innerHTML = errors.map(e=> `• ${e}`).join('<br>');
    goToStep(6);
    return;
  }else{
    box.style.display = 'none';
    enviarFormulario();
  }
}

async function enviarFormulario(){
  const form = $('#form-factura');
  const fd = new FormData(form);
  const json = {};

  fd.forEach((v,k)=> json[k]=v);

  json["tipo_documento_select"] = $('#tipo_documento_select').value;
  json["documento_select"]      = $('#documento_select').value;

  const tipoItemSel = $('.tipo_item_select');
  if(tipoItemSel) json["tipo_item_select"] = tipoItemSel.value;

  json["monto_descuento"]    = $('#monto_descuento').textContent;
  json["descuento_gravado"]  = asNumber($('#descuento_gravado').value, 0);
  json["nombre_responsable"] = $('#nombre_responsable').value;
  json["documento_responsable"] = $('#documento_responsable').value;

  // Productos
  const productos_ids = [], cantidades=[], totales_incl=[], descuentos=[];
  $$('#tabla-productos tbody tr:not(.empty-row)').forEach(row=>{
    productos_ids.push(row.getAttribute('data-id'));
    cantidades.push(row.querySelector('.cantidad-input').value);
    totales_incl.push(row.querySelector('.total-incl').textContent);
    descuentos.push(asNumber(row.querySelector('.descuento-item').textContent.replace('%',''),0)/100);
  });
  json["productos_ids"]   = productos_ids;
  json["cantidades"]      = cantidades;
  json["montos_totales"]  = totales_incl;
  json["descuento_select"]= descuentos;
  json["saldo_favor_input"]= $('#saldo_favor_input').value;

  // Formas de pago (IDs listadas)
  const formas_pago_id = [];
  $$('#tabla-formaspago-modal tbody tr').forEach(row=> formas_pago_id.push(row.getAttribute('data-id')));
  json["formas_pago_ids"] = formas_pago_id;

  // Retenciones
  json["retencion_iva"] = $('#retencion_iva_checkbox').checked;
  json["porcentaje_retencion_iva"] = $('#porcentaje_retencion_iva')?.value || 0;
  const retIva = [];
  $$('.retencion-iva-checkbox:checked').forEach(cb=> retIva.push(cb.value));
  json["productos_retencion_iva"] = retIva;

  json["retencion_renta"] = $('#retencion_renta_checkbox').checked;
  json["porcentaje_retencion_renta"] = $('#porcentaje_retencion_renta')?.value || 0;
  const retRenta = [];
  $$('.retencion-renta-checkbox:checked').forEach(cb=> retRenta.push(cb.value));
  json["productos_retencion_renta"] = retRenta;

  json["no_gravado"] = $('#no_gravado_checkbox').checked;

  // Facturas relacionadas
  json["facturas_relacionadas"] = facturasRelacionadas;

  try{
    const resp = await fetch('/fe/generar/', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify(json)
    });
    if(!resp.ok){
      const txt = await resp.text();
      throw new Error(`Error ${resp.status}: ${txt}`);
    }
    const data = await resp.json();
    if(data.redirect){
      window.location.href = data.redirect;
    }else{
      toast("Factura generada con éxito. ID: " + data.factura_id);
      $('#numero_control_input').value = data.numero_control || $('#numero_control_input').value;
    }
  }catch(err){
    console.error('generar', err);
    toast("Error de conexión: " + err.message);
  }
}
