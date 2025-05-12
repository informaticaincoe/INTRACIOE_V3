import React, { useEffect, useState } from 'react';
import {
  ProductoResponse,
  TipoUnidadMedida,
} from '../../../../../shared/interfaces/interfaces';
import {
  getAllProducts,
  getAllTipoItem,
  getAllUnidadesDeMedida,
} from '../../../../../shared/services/productos/productosServices';
import { Input } from '../../../../../shared/forms/input';
import { Dropdown } from 'primereact/dropdown';
import {
  DetalleCompraDefault,
  DetalleCompraPayload,
  errorProductoModalCompra,
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
  const [errores, setErrores] = useState(errorProductoModalCompra);

  useEffect(() => {
    if (detalleToEdit) {
      console.log("DETALLE TO EDIT",detalleToEdit)
      setNewDetalle(detalleToEdit); //Agrega la info que se va a editar si vien un id como parametro
    } else {
      setNewDetalle(DetalleCompraDefault); //Asignar un objeto por defecto ya que se agregara nueva informacion
    }
  }, [detalleToEdit]);

  useEffect(() => {
    getAllProducts().then((r) => setProductosLista(r.results));
    getAllUnidadesDeMedida().then((r) => setUnidadMedida(r));
    getAllTipoItem().then((r) => { setTipoItem(r), console.log(r) })
  }, []);

  const handleChange = (e: any) => {
    const { name, value } = e.target;
    setNewDetalle(prev => ({ ...prev, [name]: value }));
  };

  const addAndClose = (e: React.FormEvent) => {
    e.preventDefault();

    // 1) Validar
    const newErrors = {
      codigo: '',
      descripcion: '',
      cantidad: '',
      precio_unitario: '',
      tipo_item: '',
      precio_venta: '',
      categoria: '',
      preunitario: ''
    };
    console.log("newDetail", newDetalle)
    if (!newDetalle.codigo) newErrors.codigo = 'Código es un campo requerido';
    if (!newDetalle.descripcion) newErrors.descripcion = 'Descripción es un campo requerido';
    if (!newDetalle.cantidad) newErrors.cantidad = 'Cantidad es un campo requerido';
    if (!newDetalle.precio_unitario) newErrors.precio_unitario = 'Precio unitario es requerido';
    if (!newDetalle.precio_venta) newErrors.precio_venta = 'Precio venta es requerido';
    if (!newDetalle.tipo_item) newErrors.tipo_item = 'Tipo de ítem es requerido';

    setErrores(newErrors);

    // 2) Si hay algún error, detenemos aquí
    const hasError = Object.values(newErrors).some((msg) => msg !== '');
    if (hasError) {
      return;
    }

    // 3) No hubo errores: actualizar o agregar
    if (detalleToEdit && onUpdate) {
      onUpdate(newDetalle);
    } else {
      const detalleConId = {
        ...newDetalle,
        id: Date.now(), // Generar id si es nuevo
        preunitario: newDetalle.precio_unitario,
      };
      onAdd(detalleConId);
    }

    // 4) Limpiar y cerrar
    setNewDetalle(DetalleCompraDefault);
    setErrores(errorProductoModalCompra);
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
            className={`${errores.precio_venta ? 'border border-red-600' : ''}`}
          />
          {errores.codigo && <span className="text-red-500">{errores.codigo}</span>}
        </span>
        <span className="flex flex-col">
          <label htmlFor="">Descripción</label>
          <Input
            name="descripcion"
            value={newDetalle.descripcion}
            onChange={handleChange}
            placeholder="Ej. Tornillo cabeza hexagonal"
            className={`${errores.precio_venta ? 'border border-red-600' : ''}`}
          />
          {errores.descripcion && <span className="text-red-500">{errores.descripcion}</span>}
        </span>
        <span className="flex flex-col">
          <label htmlFor="">Cantidad</label>
          <Input
            type="number"
            name="cantidad"
            value={newDetalle.cantidad}
            onChange={handleChange}
            placeholder="Ej. 10"
            className={`${errores.precio_venta ? 'border border-red-600' : ''}`}
          />
          {errores.cantidad && <span className="text-red-500">{errores.cantidad}</span>}
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
            className={`${errores.precio_venta ? 'border border-red-600' : ''}`}
          />
          {errores.precio_unitario && <span className="text-red-500">{errores.precio_unitario}</span>}
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
            className={`${errores.precio_venta ? 'border border-red-600' : ''}`}
          />
          {errores.precio_venta && <span className="text-red-500">{errores.precio_venta}</span>}
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
            value={newDetalle.tipo_item}
            options={tipoItem}
            optionLabel="descripcion"
            optionValue="id"
            placeholder="Seleccionar tipo de ítem"
            onChange={e =>
              handleChange({ target: { name: 'tipo_item', value: e.value } })
            }
            className={`${errores.tipo_item ? 'p-invalid':''}`}

          />
          {errores.tipo_item && <span className="text-red-500">{errores.tipo_item}</span>}
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
