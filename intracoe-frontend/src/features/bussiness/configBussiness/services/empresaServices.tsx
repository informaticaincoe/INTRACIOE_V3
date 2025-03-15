import axios from "axios";
import { Empresa } from "../interfaces/empresaInterfaces"


const BASEURL = import.meta.env.VITE_URL_BASE;

export const getAllEmpresas = async () => {
    try {
        const response = await axios.get(`${BASEURL}/emisor/`, {
            headers: {
                'Content-Type': 'application/json', // Asegúrate de que se está enviando como JSON
            },
        });
        console.log(response.data);
        return response.data;
    } catch (error) {
        console.log(error);
    }
}

export const getEmpresaById = (id: number) => {
    console.log(id)
}

export const createEmpresaById = async (data: Empresa) => {
    try {
        const response = await axios.post(`${BASEURL}/emisor/crear/`, data, {
            headers: {
                'Content-Type': 'application/json', // Asegúrate de que se está enviando como JSON
            },
        });
        console.log(response);
        return response;
    } catch (error) {
        console.log(error);
    }
}   