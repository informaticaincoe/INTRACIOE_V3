import React, { useEffect, useState } from 'react'

import { Dialog } from 'primereact/dialog'
import { getDetalleDevolucionVentaById } from '../services/devolucionVentaServices'
import { Divider } from 'primereact/divider'
import { DevolucionVentaDetalleInterface } from '../interface/devolucionVentaInterface'

interface ModalDetallesDevolucionesVentaProp {
  data: any,
  visible: boolean,
  setVisible: any
}

export const ModalDetallesDevolucionesVenta: React.FC<ModalDetallesDevolucionesVentaProp> = ({ data, visible, setVisible }) => {
  const [detalle, setDetalle] = useState<DevolucionVentaDetalleInterface>()
  useEffect(() => {
    fetchDetallesDevolucion()
  }, [data])

  const fetchDetallesDevolucion = async () => {
    try {
      const response = await getDetalleDevolucionVentaById(data.id)
      console.log("BBBBBBBBBBBBBBBBBBB", response)
      setDetalle(response)
    } catch (error) {
      console.log(error)
    }
  }

  return (
    <Dialog header="Devolución de venta" visible={visible} onHide={() => { if (!visible) return; setVisible(false); }}
      style={{ width: '40vw' }} breakpoints={{ '1679px': '60vw', '1462px': '60vw', }}>
      {data ? (
        <div>
          <div className="p-4 gap-y-3 gap-x-5 grid grid-cols-[auto_1fr]">
            <strong>Factura:</strong>
            <span>{data.num_factura}</span>

            <strong>Fecha:</strong>
            <span>{data.fecha}</span>

            <strong>Motivo:</strong>
            <span>{data.motivo}</span>

            <strong>Estado:</strong>
            <span>{data.estado}</span>

            <strong>usuario:</strong>
            <span>{data.usuario}</span>
          </div>
          <div className='flex flex-col w-full p-4 '>
            <h1 className='text-lg font-semibold'>DETALLES</h1>
            <Divider />
          </div>
          {detalle &&
            <div className="px-4 gap-y-3 gap-x-5 grid grid-cols-[auto_1fr]">
              <strong>Producto:</strong>
              <span>{detalle.nombreProducto}</span>

              <strong>Cantidad:</strong>
              <span>{detalle.cantidad}</span>

              <strong>Motivo:</strong>
              <span>{detalle.motivo_detalle}</span>

            </div>
          }
        </div>

      ) : (
        <p>Cargando información del movimiento...</p>
      )}
    </Dialog>
  )
}
