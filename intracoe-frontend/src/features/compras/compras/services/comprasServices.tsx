import { ComprasParams } from "../../../../shared/interfaces/interfacesPagination";
import { apiInventory } from "../../../../shared/services/apiInventory";
import { getProductById } from "../../../inventario/products/services/productsServices";
import { getProveedoresById } from "../../../ventas/proveedores/services/proveedoresServices";
import { CompraInterface, detalleCompraInterfaz } from "../interfaces/comprasInterfaces";

export const getAllCompras = async (
  { page, limit }: ComprasParams = {
    page: 1,
    limit: 10,
  }
) => {
  const queryParams = new URLSearchParams();

    //paginacion
    queryParams.append('page', String(page));
    queryParams.append('page_size', String(limit));

  try {
    const response = await apiInventory.get<CompraInterface>('/compras/', {
      params: { page: 1, page_size: limit }
    });
    
    const compras = response.data.results

    const comprasConNombreProducto = await Promise.all(compras.map(async (compra) => {
      const proveedor = await getProveedoresById(compra.proveedor);
      return {
        ...compra,
        nombreProveedor: proveedor?.nombre ?? ""
      };
    }));

    console.log(comprasConNombreProducto);

    return {
      results: comprasConNombreProducto,
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

export const getComprasById = async (id: string) => {
  try {
    const response = await apiInventory.get<CompraInterface>(`/compras/${id}/`,);
    console.log(response.data)
    return response.data;
  } catch (error: any) {
    console.error(error)
  }
};

export const addCompra = async (data: any) => {
  console.log("data", data)
  try {
    const response = await apiInventory.post<CompraInterface>(`/compras/crear/`, data);
    console.log(response.data)
    return response.data;
  } catch (error: any) {
    console.error(error)
  }
};

export const updateComprasById = async (id: string, data: any) => {
  try {
    const response = await apiInventory.put<CompraInterface>(`/compras/${id}/editar/`, data);
    console.log(response.data)
    return response.data;
  } catch (error: any) {
    console.error(error)
  }
};

export const deleteComprasById = async (id: string) => {
  try {
    const response = await apiInventory.delete<CompraInterface>(`/compras/${id}/eliminar/`,);
    console.log(response.data)
    return response.data;
  } catch (error: any) {
    console.error(error)
  }
};

export const getDetalleCompras = async (id: string | number) => {
  try {
    const response = await apiInventory.get<detalleCompraInterfaz[]>(`/compras/${id}/detalles/`, {
      params: {}
    });

    const data = response.data

    const detallesConNombreProducto = await Promise.all(data.map(async (detalle) => {
      const producto = await getProductById(detalle.producto);
      return {
        ...detalle,
        nombreProducto: producto.descripcion ?? ""
      }
    }))

    return detallesConNombreProducto

  } catch (error: any) {
    console.error(error)
  }
};
