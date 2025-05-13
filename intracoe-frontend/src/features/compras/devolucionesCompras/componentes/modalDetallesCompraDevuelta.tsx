import React, { useEffect, useState } from 'react';

import { Dialog } from 'primereact/dialog';
import { compraResult } from '../../compras/interfaces/comprasInterfaces';
import { getComprasById } from '../../compras/services/comprasServices';
import { getProveedoresById } from '../../../ventas/proveedores/services/proveedoresServices';
import { ProveedorResultInterface } from '../../../ventas/proveedores/interfaces/proveedoresInterfaces';
import LoadingScreen from '../../../../shared/loading/loadingScreen';

interface ModalDetallesCompraProp {
  id: string;
  visible: boolean;
  setVisible: any;
}

export const ModalDetallesCompraDevuelta: React.FC<ModalDetallesCompraProp> = ({
  id,
  visible,
  setVisible,
}) => {
  const [data, setData] = useState<compraResult>()
  const [proveedor, setProveedor] = useState<ProveedorResultInterface>()
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchCompraData()
  }, [id])

  useEffect(() => {
    if (!visible) {
      setData(undefined);
      setProveedor(undefined);
    }
  }, [visible]);


  const fetchCompraData = async () => {
    setLoading(true);
    try {
      // 1) Trae la compra
      const comp = await getComprasById(id);
      setData(comp);

      // 2) Usa comp.proveedor directamente, no data.proveedor
      if (comp && comp.proveedor) {
        const prov = await getProveedoresById(comp.proveedor);
        setProveedor(prov);
      }
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  // const fetchNombreProveedor = async () => {
  //   console.log("ID proveedor", data?.proveedor)
  //   try {
  //     const response = await getProveedoresById(data?.proveedor ?? "")
  //     setProveedor(response)
  //   } catch (error) {
  //     console.log(error)
  //   }
  // }

  const handleClose = () => {
    setVisible(false);
    setData(undefined);
    setProveedor(undefined);
  };

  return (
    <>
      {loading && <LoadingScreen />}
      <Dialog
        header={
          <span className="flex justify-between">
            <p>Detalle compra</p>
          </span>
        }
        visible={visible}
        onHide={handleClose}
        style={{ width: '40vw' }}
        breakpoints={{ '1679px': '60vw', '1462px': '60vw' }}
      >
        {data ? (
          <div>
            <div className="grid grid-cols-[auto_1fr] gap-x-5 gap-y-3 p-4">
              {data.numero_documento &&
                <>
                  <strong>Factura:</strong>
                  <span>{data.numero_documento}</span>
                </>
              }

              <strong>Fecha:</strong>
              <span>{data.fecha}</span>

              <strong>Total:</strong>
              <span>$ {data.total}</span>

              <strong>Estado:</strong>
              <span>{data.estado}</span>

              <strong>Proveedor:</strong>
              <span>{proveedor?.nombre ?? "-"}</span>
            </div>

          </div>
        ) : (
          <p>Cargando información del movimiento...</p>
        )}
      </Dialog>
    </>
  );
};
