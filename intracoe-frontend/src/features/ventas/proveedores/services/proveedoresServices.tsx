import { apiInventory } from "../../../../shared/services/apiInventory";
import { ProveedorInterface } from "../interfaces/proveedoresInterfaces";

export const getAllProveedores = async () => {
  try {
    const response = await apiInventory.get<ProveedorInterface[]>('/proveedores/',);

    return response.data;
  } catch (error: any) {
    console.error(error)
  }
};

export const getProveedoresById = async (id: string) => {
  try {
    const response = await apiInventory.get<ProveedorInterface>(`/proveedores/${id}/`,);
    console.log(response.data)
    return response.data;
  } catch (error: any) {
    console.error(error)
  }
};

export const addProveedor = async (data:any) => {
  try {
    const response = await apiInventory.post<ProveedorInterface>(`/proveedores/crear/`,data);
    console.log(response.data)
    return response.data;
  } catch (error: any) {
    console.error(error)
  }
};

export const updateProveedoresById = async (id: string, data:any) => {
  try {
    const response = await apiInventory.put<ProveedorInterface>(`/proveedores/${id}/editar/`,data);
    console.log(response.data)
    return response.data;
  } catch (error: any) {
    console.error(error)
  }
};

export const deleteProveedoresById = async (id: string) => {
  try {
    const response = await apiInventory.delete<ProveedorInterface>(`/proveedores/${id}/eliminar/`,);
    console.log(response.data)
    return response.data;
  } catch (error: any) {
    console.error(error)
  }
};

