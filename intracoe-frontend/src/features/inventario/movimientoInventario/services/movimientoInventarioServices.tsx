import { apiInventory } from '../../../../shared/services/apiInventory';
import { movimientoInterface } from '../interfaces/movimientoInvetarioInterface';

export const getAllMovimientosInventario = async () => {
  try {
    const response = await apiInventory.get<movimientoInterface[]>('/movimientos-inventario/',);
    console.log(response.data)
    return response.data;
  } catch (error: any) {
    console.error(error)
  }
};