import axios from 'axios';
import { Contingencias } from '../interfaces/contingenciaInterfaces';

const BASEURL = import.meta.env.VITE_URL_BASE;

export const GetAlEventosContingencia = async () => {

    try {
        const response = await axios.get<Contingencias>(`${BASEURL}/contingencia/`, {
            headers: {
                'Content-Type': 'application/json', // Asegúrate de que se está enviando como JSON
            },
        });

        console.log(response.data)
        console.log(response.data.results)

        return response.data;
    } catch (error) {
        console.log(error);
    }
}