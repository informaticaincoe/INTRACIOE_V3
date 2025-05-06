import React, { useEffect, useState } from 'react'

import { Dialog } from 'primereact/dialog'
import { CompraInterface } from '../interfaces/comprasInterfaces'

interface ModalDetallesCompraProp {
  data: CompraInterface,
  visible: boolean,
  setVisible: any
}

export const ModalDetallesCompra: React.FC<ModalDetallesCompraProp> = ({ data, visible, setVisible }) => {

  return (
    <Dialog header="Detalle compra" visible={visible} onHide={() => { if (!visible) return; setVisible(false); }}
      style={{ width: '40vw' }} breakpoints={{ '1679px': '60vw', '1462px': '60vw', }}>
      {data ? (
        <div>
          <div className="p-4 gap-y-3 gap-x-5 grid grid-cols-[auto_1fr]">

            <strong>Proveedor:</strong>
            <span>{data.nombreProveedor}</span>

            {/* <strong>Fecha:</strong>
            <span>{data.fecha}</span> */}
            
            <strong>Total:</strong>
            <span>{data.total}</span>

            <strong>Estado:</strong>
            <span>{data.estado}</span>
          </div>
        </div>

      ) : (
        <p>Cargando información del movimiento...</p>
      )}
    </Dialog>
  )
}
