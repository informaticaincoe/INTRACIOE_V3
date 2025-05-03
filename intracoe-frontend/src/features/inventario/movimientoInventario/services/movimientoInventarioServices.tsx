import { apiInventory } from '../../../../shared/services/apiInventory';
import { getProductById } from '../../products/services/productsServices';
import { movimientoInterface } from '../interfaces/movimientoInvetarioInterface';

export const getAllMovimientosInventario = async () => {
  try {
    const response = await apiInventory.get<movimientoInterface[]>('/movimientos-inventario/',);
    const movimientos = response.data;

    // Iteramos sobre cada movimiento para obtener el nombre del producto
    const movimientosConNombreProducto = await Promise.all(movimientos.map(async (movimiento) => {
      // Obtenemos el producto por ID
      const producto = await getProductById(movimiento.producto); // Supongo que 'productoId' es el campo que relaciona movimiento con producto
      // Devolvemos el movimiento con el nombre del producto agregado
      return {
        ...movimiento,
        nombreProducto: producto.descripcion // O el campo correspondiente a nombre
      };
    }));

    console.log(movimientosConNombreProducto);
    return movimientosConNombreProducto; 
  } catch (error: any) {
    console.error(error)
  }
};