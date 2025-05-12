import React, { useEffect, useState } from 'react';

import { Dialog } from 'primereact/dialog';
import {
  CompraInterface,
  compraResult,
  detalleCompraInterfaz,
} from '../interfaces/comprasInterfaces';
import { getDetalleCompras } from '../services/comprasServices';
import { Divider } from 'primereact/divider';
import {
  createDevolucionesCompra,
  getAllDetalleDevolucionesCompra,
} from '../../devolucionesCompras/services/devolucionesCompraServices';
import { ModalDevolucionCompra } from '../../devolucionesCompras/componentes/modalDevolucionCompra';

interface ModalDetallesCompraProp {
  data: compraResult;
  visible: boolean;
  setVisible: any;
}

export const ModalDetallesCompra: React.FC<ModalDetallesCompraProp> = ({
  data,
  visible,
  setVisible,
}) => {
  const [compra, setCompra] = useState<CompraInterface>();
  const [visibleModalAjuste, setVisibleModalAjuste] = useState(false);
  const [detalle, setDetalle] = useState<detalleCompraInterfaz[]>([
    {
      cantidad: 0,
      compra: 0,
      id: 0,
      precio_unitario: '',
      subtotal: '',
      producto: 0,
      precio_venta: ''
    },
  ]);

  useEffect(() => {
    fetchDetalleCompras();
  }, [data]);

  const fetchDetalleCompras = async () => {
    console.log('daaaaaaaaaaaaata', data);
    try {
      const response = await getDetalleCompras(data.id);
      console.log('DETALLE COMPRA', response);
      setDetalle(response ?? []);
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <Dialog
      header={
        <span className="flex justify-between">
          <p>Detalle compra</p>
          <button
            className="border-primary-blue text-primary-blue hover:bg-primary-blue mr-5 rounded-md border px-5 py-3 text-sm font-medium hover:text-white"
            onClick={() => setVisibleModalAjuste(true)}
          >
            Realizar devolución
          </button>
        </span>
      }
      visible={visible}
      onHide={() => {
        if (!visible) return;
        setVisible(false);
      }}
      style={{ width: '40vw' }}
      breakpoints={{ '1679px': '60vw', '1462px': '60vw' }}
    >
      {data ? (
        <div>
          <div className="grid grid-cols-[auto_1fr] gap-x-5 gap-y-3 p-4">
            <strong>Producto:</strong>
            <span>{data.nombreProveedor}</span>

            <strong>Fecha:</strong>
            <span>{data.fecha}</span>

            <strong>Total:</strong>
            <span>$ {data.total}</span>

            <strong>Estado:</strong>
            <span>{data.estado}</span>
          </div>
          <div className="flex w-full flex-col p-4">
            <h1 className="text-lg font-semibold">DETALLES</h1>
            <Divider />
          </div>
          {detalle &&
            <div className='grid grid-cols-2 gap-5'>
              {detalle.map((ele) => (
                <div
                  key={ele.id}
                  className="bg-white rounded-2xl shadow-sm hover:shadow-md transition-shadow duration-200 p-6 space-y-4"
                >
                  <div>
                    <h3 className="text-xl font-semibold text-gray-800">
                      {ele.nombreProducto}
                    </h3>
                    <h3 className="text-sm font- text-gray-500">
                      {ele.codigo}
                    </h3>
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-x-6 gap-y-3 text-sm text-gray-600">
                    <div className="flex flex-col">
                      <span className="font-medium text-gray-700">Cantidad</span>
                      <span>{ele.cantidad}</span>
                    </div>

                    <div className="flex flex-col">
                      <span className="font-medium text-gray-700">Precio unitario</span>
                      <span>$ {parseFloat(ele.precio_unitario).toFixed(2)}</span>
                    </div>

                    <div className="flex flex-col sm:col-span-2">
                      <span className="font-medium text-gray-700">Subtotal</span>
                      <span className="text-lg font-semibold text-gray-800">
                        $ {parseFloat(ele.subtotal).toFixed(2)}
                      </span>
                    </div>
                  </div>
                </div>

              ))}
            </div>
          }
          {
            //TODO: Pendiente ajuste
            visibleModalAjuste && detalle && (
              <ModalDevolucionCompra
                data={data}
                // productos={detalle}s
                visible={visibleModalAjuste}
                setVisible={setVisibleModalAjuste}
              />
            )
          }
        </div>
      ) : (
        <p>Cargando información del movimiento...</p>
      )}
    </Dialog>
  );
};
