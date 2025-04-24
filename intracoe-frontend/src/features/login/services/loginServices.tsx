import axios from 'axios';

const BASEURL = import.meta.env.VITE_URL_AUTENTICACION;

export const login = async (data: any) => {
    console.log(data)
    try {
        const response = await axios.post(`${BASEURL}/login/`, data);
        return response.data
    }
    catch (error: any) {
        console.log(error)
    }

};
