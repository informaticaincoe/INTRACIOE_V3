import { apiInventory } from "../../../../shared/services/apiInventory";

export const getAllDevolucionesVentas = async () => {
  try {
    const response = await apiInventory.get('/devoluciones-venta/',);
    return response.data;
  } catch (error: any) {
    console.error(error)
  }
};