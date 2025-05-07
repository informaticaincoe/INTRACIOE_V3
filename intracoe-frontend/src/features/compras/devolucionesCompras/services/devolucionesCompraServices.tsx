import { apiInventory } from "../../../../shared/services/apiInventory";
import { getProductById } from "../../../inventario/products/services/productsServices";

export const getAllDevolucionesCompra = async () => {
  try {
    const response = await apiInventory.get('/devoluciones-compra/',);
    return response.data;
  } catch (error: any) {
    console.error(error)
  }
};

export const getDetalleDevolucionCompraById = async (id: string | number) => {
  try {
    const response = await apiInventory.get(`/detalle-devolucion-compra/${id}/`);
    const detalle = response.data;

    const producto = await getProductById(detalle.producto);
    const detalleConNombre = {
      ...detalle,
      nombreProducto: producto.descripcion,
    };

    return detalleConNombre;
  } catch (error: any) {
    console.error(error);
    return null;
  }
};

export const createDevolucionesCompra = async (data:any) => {
    try {
      const response = await apiInventory.post('/devoluciones-compra/crear/', data);
      return response.data;
    } catch (error: any) {
      console.error(error)
    }
  };


