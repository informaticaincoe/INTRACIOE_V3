import axios from 'axios';

const BASEURL = import.meta.env.VITE_URL_BASE;

export const getAllFacturas = async () => {
    try {
        // Asegúrate de que el endpoint sea el correcto
        const response = await axios.get(`${BASEURL}/facturas/`);
        return response.data;
    } catch (error) {
        console.log('Error en la solicitud:', error);
    }
};