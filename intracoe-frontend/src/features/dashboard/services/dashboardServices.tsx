import { api } from '../../../shared/services/api';

export const getTotalesPorTipoDTE = () =>
  api.get('/dashboard/totales-por-tipo/').then((r) => r.data.totales_por_tipo);

export const getTotalVentas = () =>
  api.get('/dashboard/totales-ventas/').then((res) => res.data.total_ventas);

export const getClientes = () =>
  api.get('/dashboard/clientes/').then((res) => res.data.clientes);

export const getProductos = () =>
  api.get('/dashboard/productos/').then((res) => res.data.productos);
