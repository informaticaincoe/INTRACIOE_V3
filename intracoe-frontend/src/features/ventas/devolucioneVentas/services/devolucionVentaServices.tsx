import { apiInventory } from "../../../../shared/services/apiInventory";
import { getProductById } from "../../../inventario/products/services/productsServices";

export const getAllDevolucionesVentas = async () => {
  try {
    const response = await apiInventory.get('/devoluciones-venta/',);
    return response.data;
  } catch (error: any) {
    console.error(error)
  }
};

export const getDetalleDevolucionVentaById = async (id: string | number) => {
  try {
    const response = await apiInventory.get(`/detalle-devolucion-venta/${id}/`);
    const detalle = response.data;

    const producto = await getProductById(detalle.producto);
    const detalleConNombre = {
      ...detalle,
      nombreProducto: producto.descripcion,
    };

    console.log("DETALLE",detalleConNombre);
    return detalleConNombre;
  } catch (error: any) {
    console.error(error);
    return null;
  }
};

