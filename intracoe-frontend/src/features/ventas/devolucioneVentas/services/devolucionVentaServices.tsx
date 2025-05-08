import { aDevolucionVentasParams } from "../../../../shared/interfaces/interfacesPagination";
import { apiInventory } from "../../../../shared/services/apiInventory";
import { getProductById } from "../../../inventario/products/services/productsServices";

export const getAllDevolucionesVentas = async (
  { page, limit }: aDevolucionVentasParams = {
    page: 1,
    limit: 10,
  }
) => {
  const queryParams = new URLSearchParams();

  //paginacion
  queryParams.append('page', String(page));
  queryParams.append('page_size', String(limit));

  try {
    const response = await apiInventory.get('/devoluciones-venta/', {
      params: { page: page, page_size: limit }
    });

    console.log("RES¨PMSE DEVPÑUCIOPNESFd",response.data)

    return {
      results: response.data.results,
      current_page: response.data.current_page,
      page_size: response.data.page_size,
      has_next: response.data.has_next,
      has_previous: response.data.has_previous,
      count: response.data.count
    };
  } catch (error: any) {
    console.error(error)
  }
};
export const getDetalleDevolucionVentaById = async (id: string | number,  page = 1,
  limit = 10,)  => {
  try {
    const response = await apiInventory.get(`/detalle-devolucion-venta/${id}/`);
    const detalle = response.data;

    const producto = await getProductById(detalle.producto);
    const detalleConNombre = {
      ...detalle,
      nombreProducto: producto.descripcion,
    };

    console.log("DETALLE", detalleConNombre);
    return detalleConNombre;
  } catch (error: any) {
    console.error(error);
    return null;
  }
};

