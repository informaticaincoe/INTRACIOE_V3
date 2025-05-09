import React, { useEffect, useState } from 'react';
import {
  ProductoResponse,
  TipoUnidadMedida,
} from '../../../../../shared/interfaces/interfaces';
import {
  getAllProducts,
  getAllUnidadesDeMedida,
} from '../../../../../shared/services/productos/productosServices';
import { Input } from '../../../../../shared/forms/input';
import { Dropdown } from 'primereact/dropdown';
import {
  DetalleCompraDefault,
  DetalleCompraPayload,
  tipoCompraOptions,
} from '../../interfaces/comprasInterfaces';
import { Dialog } from 'primereact/dialog';

interface ModalDetallesProductosProps {
  visible: boolean;
  setVisible: (v: boolean) => void;
  onAdd: (detalle: DetalleCompraPayload) => void;
  detalleToEdit?: DetalleCompraPayload | null;
  onUpdate?: (detalle: DetalleCompraPayload) => void;
}

export const ModalDetallesProductos: React.FC<ModalDetallesProductosProps> = ({
  visible,
  setVisible,
  onAdd,
  detalleToEdit,
  onUpdate,
}) => {
  const [productosLista, setProductosLista] = useState<ProductoResponse[]>([]);
  const [unidadMedida, setUnidadMedida] = useState<TipoUnidadMedida[]>([]);
    const [tipoItem, setTipoItem] = useState();
  const [newDetalle, setNewDetalle] =
    useState<DetalleCompraPayload>(DetalleCompraDefault);

  useEffect(() => {
    if (detalleToEdit) {
      setNewDetalle(detalleToEdit);
    } else {
      setNewDetalle(DetalleCompraDefault);
    }
  }, [detalleToEdit]);

  useEffect(() => {
    getAllProducts().then((r) => setProductosLista(r.results));
    getAllUnidadesDeMedida().then((r) => setUnidadMedida(r));
  }, []);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement> | any) => {
    const { name, value } = e.target;
    setNewDetalle((prev) => ({ ...prev, [name]: value }));
  };

  const addAndClose = (e: React.FormEvent) => {
    e.preventDefault();

    if (detalleToEdit && onUpdate) {
      onUpdate(newDetalle); // Editar
    } else {
      const detalleConId = {
        ...newDetalle,
        id: Date.now(), // Generar id si es nuevo
        preunitario: newDetalle.precio_unitario,
      };
      onAdd(detalleConId); // Agregar nuevo
    }

    setNewDetalle(DetalleCompraDefault);
    setVisible(false);
  };

  return (
    <Dialog
      header="Agregar detalle de producto"
      visible={visible}
      onHide={() => setVisible(false)}
      style={{ width: '40vw' }}
    >
      <form onSubmit={addAndClose} className="flex flex-col gap-5 px-5">
        <span className="flex flex-col">
          <label htmlFor="">Codigo</label>
          <Input
            name="codigo"
            value={newDetalle.codigo}
            onChange={handleChange}
            placeholder="Ej. PROD-00123"
          />
        </span>
        <span className="flex flex-col">
          <label htmlFor="">Descripción</label>

          <Input
            name="descripcion"
            value={newDetalle.descripcion}
            onChange={handleChange}
            placeholder="Ej. Tornillo cabeza hexagonal"
          />
        </span>
        <span className="flex flex-col">
          <label htmlFor="">Cantidad</label>

          <Input
            type="number"
            name="cantidad"
            value={newDetalle.cantidad}
            onChange={handleChange}
            placeholder="Ej. 10"
          />
        </span>

        <span className="flex flex-col">
          <label htmlFor="">Precio unitario</label>
          <Input
            type="number"
            name="precio_unitario"
            value={newDetalle.precio_unitario}
            onChange={handleChange}
            placeholder="Ej. 15.50"
            step="0.01"
          />
        </span>

        <span className="flex flex-col">
          <label htmlFor="">Precio venta</label>
          <Input
            type="number"
            name="precio_venta"
            value={newDetalle.precio_venta}
            onChange={handleChange}
            placeholder="Ej. 18.00"
            step="0.01"
          />
        </span>

        <span className="flex flex-col">
          <label htmlFor="">Unidad de medida</label>
          <Dropdown
            name="unidad_medida"
            value={newDetalle.unidad_medida}
            options={unidadMedida}
            optionLabel="descripcion"
            optionValue="id"
            placeholder="Seleccionar unidad..."
            onChange={handleChange}
          />
        </span>

        <span className="flex flex-col">
          <label htmlFor="">Tipo compra</label>
          <Dropdown
            name="tipo_compra"
            value={newDetalle.tipo_compra}
            options={tipoCompraOptions}
            optionLabel="label"
            optionValue="value"
            placeholder="Seleccionar tipo..."
            onChange={handleChange}
          />
        </span>

        <span className="flex flex-col">
          <label htmlFor="">Tipo item</label>
          <Dropdown
            name="tipo_item"
            value={formData.tipo_item}
            onChange={(e) =>
              handleChange({ target: { name: 'tipo_item', value: e.value } })
            }
            options={tipoItem}
            optionLabel="descripcion"
            optionValue="id"
            placeholder="Seleccionar el tipo de item"
            className="md:w-14rem w-full text-start"
          />
        </span>

        <button
          type="submit"
          className="bg-primary-blue self-start rounded-md px-8 py-3 text-white"
        >
          Agregar producto
        </button>
      </form>
    </Dialog>
  );
};
