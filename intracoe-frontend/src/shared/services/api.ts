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

// Redirige a /login si no hay token o si hay error 401 o 403
api.interceptors.response.use(
  response => response,
  error => {
    const status = error.response?.status;

    if (status === 401 || status === 403) {
      document.cookie = 'authToken=; max-age=0; path=/';
      window.location.href = '/login';
    }

    return Promise.reject(error);
  }
);
