import React, { useEffect, useState } from 'react';
import { compraResult } from '../../compras/interfaces/comprasInterfaces';
import { Dialog } from 'primereact/dialog';
import { Divider } from 'antd';
import { createDevolucionesCompra } from '../services/devolucionesCompraServices';

interface ModalDetallesCompraProp {
  data: compraResult;
  visible: boolean;
  setVisible: any;
}

export const ModalDevolucionCompra: React.FC<ModalDetallesCompraProp> = ({
  data,
  visible,
  setVisible,
}) => {
  const [detalle, setDetalel] = useState();
  useEffect(() => {
    console.log('DATA', data);
  }, [data]);

  const handleRealizarDevolucion = async () => {
    const devolucionData = {
      compra: data.id, //id compra
      detalles: [
        {
          cantidad: 8,
          producto: 1,

          motivo_detalle: 'Falla técnica',
        },
      ],
      motivo: 'pruebas',
      estado: 'Pendiente',
      usuario: 'admin',
    };
    try {
      const response = await createDevolucionesCompra(data);
      console.log('DDDDDDDDDDDDDDDDD', response);
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <Dialog
      header={
        <span className="flex justify-between">
          <p>Realizar devolución</p>
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
      <p>data</p>
    </Dialog>
  );
};
