import axios from 'axios';

const BASEURL = import.meta.env.VITE_URL_BASE;

export const getAllTipoDte = async () => {
  try {
    const response = await axios.get(`${BASEURL}/tipo-dte/`);
    console.log(response)
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const getAllCondicionDeOperacion = async () => {
  try {
    const response = await axios.get(`${BASEURL}/condicion-operacion/`);
    return response.data
  } catch (error) {
    throw new Error()
  }
}

export const getAllModelosDeFacturacion = async () => {
  try {
    const response = await axios.get(`${BASEURL}/modelo-facturacion/`);
    return response.data
  } catch (error) {
    throw new Error()
  }
}

export const getAllTipoTransmision = async () => {
  try {
    const response = await axios.get(`${BASEURL}/tipo-transmision/`);
    return response.data
  } catch (error) {
    throw new Error()
  }
}

export const getAllMetodosDePago = async () =>{
  try {
    const response = await axios.get(`${BASEURL}/formas-pago/`);
    return response.data
  } catch (error) {
    console.log(error)
  }
}
