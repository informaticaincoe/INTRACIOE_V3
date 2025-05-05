import React, { useEffect, useState } from 'react'

import { Dialog } from 'primereact/dialog'
import { AjusteInventarioInterface } from '../interfaces/ajusteInventarioInterfaces'

interface ModalDetalleAjusteMovimientoInventarioProp {
  data: AjusteInventarioInterface,
  visible: boolean,
  setVisible: any
}

export const ModalDetalleAjusteMovimientoInventario: React.FC<ModalDetalleAjusteMovimientoInventarioProp> = ({ data, visible, setVisible }) => {


  return (
    <Dialog header="Detalle Ajuste de inventario" visible={visible} onHide={() => { if (!visible) return; setVisible(false); }}
      style={{ width: '40vw' }} breakpoints={{ '1679px': '60vw', '1462px': '60vw', }}>
      {data ? (
        <div>
          <div className="p-4 gap-y-3 gap-x-5 grid grid-cols-[auto_1fr]">

            <strong>Producto:</strong>
            <span>{data.nombreProducto}</span>

            <strong>Usuario:</strong>
            <span>{data.usuario}</span>

            <strong>Cantidad ajustada:</strong>
            <span>{data.cantidad_ajustada}</span>

            <strong>Fecha:</strong>
            <span>{new Date(data.fecha).toLocaleDateString()}</span>

            <strong>Motivo:</strong>
            <span>{data.motivo}</span>

            <strong>Almacen:</strong>
            <span>{data.nombreAlmacen}</span>

          </div>
        </div>

      ) : (
        <p>Cargando información del movimiento...</p>
      )}
    </Dialog>
  )
}
