import axios from 'axios';
import { getCookie } from 'typescript-cookie';

export const api = axios.create({
  baseURL: import.meta.env.VITE_URL_BASE,
  withCredentials: true,
});

// Agrega el token a cada petición
api.interceptors.request.use((cfg) => {
  const token = getCookie('authToken');
  if (token && cfg.headers) {
    cfg.headers.Authorization = `Token ${token}`;
  }
  return cfg;
});

// **Nuevo** interceptor de respuestas
// api.interceptors.response.use(
//   response => response,
//   error => {
//     // Extraemos el mensaje de error según tu backend
//     const msg = error.response?.data?.error
//              || error.response?.data?.detail
//              || error.response?.data;

//     // Si es el caso "Error interno del servidor", redirigimos al login
//     if (msg === 'Error interno del servidor' || error.response?.status === 500) {
//       // Limpiar token/cookies si fuera necesario
//       document.cookie = 'authToken=; max-age=0; path=/';
//       // Redirige a la ruta de login
//       window.location.href = '/login';
//     }

//     // Siempre rechaza la promesa para que los catch sigan funcionando
//     return Promise.reject(error);
//   }
// );
