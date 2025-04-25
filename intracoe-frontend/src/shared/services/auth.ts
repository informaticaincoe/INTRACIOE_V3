// src/shared/services/auth.ts
import axios from 'axios';
import { getCookie, setCookie, removeCookie } from 'typescript-cookie';

export const authApi = axios.create({
  baseURL: import.meta.env.VITE_URL_AUTENTICACION,
  withCredentials: true,
});

// -------------------
// 1) Interceptor de petición
// -------------------
authApi.interceptors.request.use((config) => {
  const token = getCookie('authToken');
  if (token) {
    config.headers = config.headers ?? {};
    // DRF TokenAuthentication espera "Token <key>"
    config.headers.Authorization = `Token ${token}`;
  }
  return config;
});

// -------------------
// 2) Interceptor de respuesta para login
// -------------------
authApi.interceptors.response.use((resp) => {
  // Al hacer login, guardamos el token en cookie
  if (resp.config.url?.endsWith('/login/') && resp.data.token) {
    setCookie('authToken', resp.data.token, {
      expires: 1,
      secure: true,
      sameSite: 'Lax',
      path: '/',
    });
  }
  return resp;
});
