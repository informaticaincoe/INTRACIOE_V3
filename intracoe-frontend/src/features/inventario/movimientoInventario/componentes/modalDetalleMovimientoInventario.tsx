import React, { useEffect, useState } from 'react';
import { movimientoInterface } from '../interfaces/movimientoInvetarioInterface';
import { Dialog } from 'primereact/dialog';
import { getMovimientosInventarioById } from '../services/movimientoInventarioServices';
import { ModalRealizarAjuste } from '../../ajusteInventario/componentes/modalRealizarAjuste';

interface ModalDetalleMovimientoInventarioProp {
  id: string | number;
  visible: boolean;
  setVisible: any;
}

export const ModalDetalleMovimientoInventario: React.FC<
  ModalDetalleMovimientoInventarioProp
> = ({ id, visible, setVisible }) => {
  const [movimientoInventario, setMovimientoInvetario] =
    useState<movimientoInterface>();
  const [visibleModalAjuste, setVisibleModalAjuste] = useState(false);

  useEffect(() => {
    fetchMovimientoInventarioById();
  }, [id]);

  const fetchMovimientoInventarioById = async () => {
    try {
      const response = await getMovimientosInventarioById(id);
      setMovimientoInvetario(response);
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <Dialog
      header="Detalle movimiento de inventario"
      visible={visible}
      onHide={() => {
        if (!visible) return;
        setVisible(false);
      }}
      style={{ width: '40vw' }}
      breakpoints={{ '1679px': '60vw', '1462px': '60vw' }}
    >
      {movimientoInventario ? (
        <div>
          <div className="grid grid-cols-[auto_1fr] gap-x-5 gap-y-3 p-4">
            <strong>Tipo:</strong>
            <span>{movimientoInventario.tipo}</span>

            <strong>Referencia:</strong>
            <span>{movimientoInventario.referencia}</span>

            <strong>Producto:</strong>
            <span>{movimientoInventario.nombreProducto}</span>

            <strong>Almacén:</strong>
            <span>{movimientoInventario.nombreAlmacen}</span>

            <strong>Cantidad:</strong>
            <span>{movimientoInventario.cantidad}</span>

            <strong>Fecha:</strong>
            <span>
              {new Date(movimientoInventario.fecha).toLocaleDateString()}
            </span>
          </div>
          <span onClick={() => setVisibleModalAjuste(true)}>
            <button className="border-primary-blue text-primary-blue rounded-md border px-5 py-2">
              Realizar ajuste
            </button>
          </span>

          {visibleModalAjuste && movimientoInventario && (
            <ModalRealizarAjuste
              data={movimientoInventario} // Solo pasa un ID válido si hay un producto seleccionado
              visible={visibleModalAjuste}
              setVisible={setVisibleModalAjuste}
            />
          )}
        </div>
      ) : (
        <p>Cargando información del movimiento...</p>
      )}
    </Dialog>
  );
};
