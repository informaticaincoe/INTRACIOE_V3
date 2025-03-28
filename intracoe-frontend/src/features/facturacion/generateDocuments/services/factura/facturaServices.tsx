import axios from 'axios';

const BASEURL = import.meta.env.VITE_URL_BASE;

export const generarFacturaService = async (data:any) => {
    console.log("data", data)
    try {
      const response = await axios.post(`${BASEURL}/factura/generar/`, data);
      console.log("response.data", response.data)
      return response.data;
    } catch (error) {
        console.log(error)
      throw new Error();
    }
  };

  export const getFacturaCodigos = async () => {
    try {
      const response = await axios.get(`${BASEURL}/factura/generar/`);
      console.log("response.data", response.data)
      return response.data;
    } catch (error) {
        console.log(error)
      throw new Error();
    }
  };
  