import { apiInventory } from "../../../../shared/services/apiInventory";
import { CompraInterface } from "../interfaces/comprasInterfaces";

export const getAllCompras = async () => {
  try {
    const response = await apiInventory.get<CompraInterface[]>('/compras/',);

    return response.data;
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

export const addCompra = async (data:any) => {
  try {
    const response = await apiInventory.post<CompraInterface>(`/compras/crear/`,data);
    console.log(response.data)
    return response.data;
  } catch (error: any) {
    console.error(error)
  }
};

export const updateComprasById = async (id: string, data:any) => {
  try {
    const response = await apiInventory.put<CompraInterface>(`/compras/${id}/editar/`,data);
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

