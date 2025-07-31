import { ComprasParams } from '../../../../shared/interfaces/interfacesPagination';
import { apiInventory } from '../../../../shared/services/apiInventory';
import { getProductById } from '../../../inventario/products/services/productsServices';
import { getProveedoresById } from '../../../ventas/proveedores/services/proveedoresServices';
import {
  CompraInterface,
  compraResult,
  DetalleCompraInterfaz,
} from '../interfaces/comprasInterfaces';

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
      params: { page: page, page_size: limit },
    });

    const compras = response.data.results;

    const comprasConNombreProducto = await Promise.all(
      compras.map(async (compra) => {
        const proveedor = await getProveedoresById(compra.proveedor);
        return {
          ...compra,
          nombreProveedor: proveedor?.nombre ?? '',
        };
      })
    );

    console.log(comprasConNombreProducto);

    return {
      results: comprasConNombreProducto,
      current_page: response.data.current_page,
      page_size: response.data.page_size,
      has_next: response.data.has_next,
      has_previous: response.data.has_previous,
      count: response.data.count,
    };
  } catch (error: any) {
    console.error(error);
  }
};

export const getComprasById = async (id: string) => {
  try {
    const response = await apiInventory.get<compraResult>(`/compras/${id}/`);
    console.log(response.data);
    return response.data;
  } catch (error: any) {
    console.error(error);
  }
};

export const addCompra = async (data: any) => {
  console.log('data', data);
  try {
    const response = await apiInventory.post<compraResult>(
      `/compras/crear/`,
      data
    );
    console.log(response.data);
    return response.data;
  } catch (error: any) {
    console.error(error);
  }
};

export const updateComprasById = async (id: string, data: any) => {
  try {
    const response = await apiInventory.put<CompraInterface>(
      `/compras/${id}/editar/`,
      data
    );
    console.log(response.data);
    return response.data;
  } catch (error: any) {
    console.error(error);
  }
};

export const deleteComprasById = async (id: string) => {
  try {
    const response = await apiInventory.delete<CompraInterface>(
      `/compras/${id}/eliminar/`
    );
    console.log(response.data);
    return response.data;
  } catch (error: any) {
    console.error(error);
  }
};

export const getDetalleCompras = async (id: string | number) => {
  try {
    const response = await apiInventory.get<DetalleCompraInterfaz[]>(
      `/compras/${id}/detalles/`
    );

    const data = response.data;

    const detallesConNombreProducto = await Promise.all(
      data.map(async detalle => {
        if (!detalle.producto) {
          // devolvemos el objeto detalle tal cual, no el array completo
          return detalle;
        }
        const producto = await getProductById(detalle.producto);
        return {
          ...detalle,
          nombreProducto: producto.descripcion ?? '',
          descripcion: producto.descripcion ?? '',
          codigo: producto.codigo ?? '',
          precio_venta: producto.precio_venta ?? '',
        };
      })
    );
    console.log("DATAAAA GETDETALLECOMPRA",data)
    return detallesConNombreProducto;
  } catch (error) {
    console.error(error);
    // en caso de fallo devolvemos siempre un array vacío
    return [];
  }
};