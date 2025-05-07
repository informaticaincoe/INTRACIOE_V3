import React, { useEffect, useState } from 'react'

import { Dialog } from 'primereact/dialog'
import { CompraInterface, detalleCompraInterfaz } from '../interfaces/comprasInterfaces'
import { getDetalleCompras } from '../services/comprasServices'
import { Divider } from 'primereact/divider'

interface ModalDetallesCompraProp {
  data: CompraInterface,
  visible: boolean,
  setVisible: any
}

export const ModalDetallesCompra: React.FC<ModalDetallesCompraProp> = ({ data, visible, setVisible }) => {
  const [detalle, setDetalle] = useState<detalleCompraInterfaz[]>(
    [{
      cantidad: 0,
      compra: 0,
      id: 0,
      precio_unitario: "",
      subtotal: "",
      producto: 0
    }]
  )

  useEffect(() => {
    console.log(data)
    fetchDetalleCompras()
  }, [data])

  const fetchDetalleCompras = async () => {
    try {
      const response = await getDetalleCompras(data.id)
      setDetalle(response ?? [])
    } catch (error) {
      console.log(error)
    }
  }
  return (
    <Dialog
      header={
        <span className='flex justify-between'>
          <p>Detalle compra</p>
          <button className='text-sm font-medium border border-primary-blue text-primary-blue rounded-md px-5 py-3 mr-5 hover:bg-primary-blue hover:text-white'>Realizar devolución</button>
        </span>
      }
      visible={visible}
      onHide={() => { if (!visible) return; setVisible(false); }}
      style={{ width: '40vw' }} breakpoints={{ '1679px': '60vw', '1462px': '60vw', }}
    >
      {data ? (
        <div>
          <div className="p-4 gap-y-3 gap-x-5 grid grid-cols-[auto_1fr]">

            <strong>Producto:</strong>
            <span>{data.nombreProveedor}</span>

            <strong>Fecha:</strong>
            <span>{data.fecha}</span>

            <strong>Total:</strong>
            <span>{data.total}</span>

            <strong>Estado:</strong>
            <span>{data.estado}</span>
          </div>
          <div className='flex flex-col w-full p-4 '>
            <h1 className='text-lg font-semibold'>DETALLES</h1>
            <Divider />
          </div>
          {detalle &&
            (
              detalle.map((ele) => (
                <div className="px-4 gap-y-3 gap-x-5 grid grid-cols-[auto_1fr]">
                  <strong>Producto:</strong>
                  <span>{ele.nombreProducto}</span>

                  <strong>Cantidad:</strong>
                  <span>{ele.cantidad}</span>

                  <strong>Precio unitario:</strong>
                  <span>{ele.precio_unitario}</span>

                  <strong>Subtotal:</strong>
                  <span>{ele.subtotal}</span>
                </div>
              ))
            )
          }
        </div>


      ) : (
        <p>Cargando información del movimiento...</p>
      )
      }
    </Dialog >
  )
}
