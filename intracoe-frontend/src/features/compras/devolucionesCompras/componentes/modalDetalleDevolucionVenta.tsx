import { Dialog } from 'primereact/dialog';
import { Button } from 'primereact/button';
import React from 'react';

interface ModalDetalleDevolucionVentaProps {
  data: DevolucionCompraDetalle[];
  visible: boolean;
  setVisible: (visible: boolean) => void;
}

interface DevolucionCompraDetalle {
  cantidad: number;
  motivo_detalle: string;
  nombreProducto: string;
  producto: number;
}

export const ModalDetalleDevolucionVenta: React.FC<ModalDetalleDevolucionVentaProps> = ({
  data,
  visible,
  setVisible,
}) => {
  const handleClose = () => setVisible(false);

  return (
    <Dialog
      header="Detalle de productos devueltos"
      visible={visible}
      onHide={handleClose}
      style={{ width: '50vw', maxWidth: '90vw' }}
    >
      {data.length > 0 ? (
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-100">
              <tr>
                <th className="px-4 py-2 text-left text-sm font-semibold text-gray-700">
                  Producto
                </th>
                <th className="px-4 py-2 text-left text-sm font-semibold text-gray-700">
                  Cantidad
                </th>
                <th className="px-4 py-2 text-left text-sm font-semibold text-gray-700">
                  Motivo
                </th>
                <th className="px-4 py-2 text-center text-sm font-semibold text-gray-700">
                  ID
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-100">
              {data.map((item, idx) => (
                <tr key={idx} className="hover:bg-gray-50">
                  <td className="px-4 py-3 text-sm text-gray-800">
                    {item.nombreProducto}
                  </td>
                  <td className="px-4 py-3 text-sm text-gray-800 text-left">
                    {item.cantidad}
                  </td>
                  <td className="px-4 py-3 text-sm text-gray-800">
                    {item.motivo_detalle}
                  </td>
                  <td className="px-4 py-3 text-sm text-gray-800 text-center">
                    {item.producto}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <p className="text-gray-500 text-center py-4">
          No hay detalles de devolución disponibles.
        </p>
      )}

      <div className="flex justify-end mt-4">
        <Button
          label="Aceptar"
          icon="pi pi-check"
          onClick={handleClose}
          className="p-button-primary"
        />
      </div>
    </Dialog>
  );
};
