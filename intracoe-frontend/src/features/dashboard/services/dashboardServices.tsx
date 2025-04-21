import axios from 'axios';

const BASEURL = import.meta.env.VITE_URL_BASE;

export const getTotalesPorTipoDTE = async () => {
    const response = await axios.get(`${BASEURL}/facturas/totales-por-tipo/`);
    return response.data.totales_por_tipo;
};

export const getTotalVentas = async () => {
    const response = await axios.get(`${BASEURL}/facturas/totales-ventas/`);
    return response.data.total_ventas;
}

export const getClientes = async () => {
    const response = await axios.get(`${BASEURL}/facturas/clientes/`);
    return response.data.clientes;
}

export const getProductos = async () => {
    const response = await axios.get(`${BASEURL}/facturas/productos/`);
    return response.data.productos;
}