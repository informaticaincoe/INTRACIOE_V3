// src/services/api.ts
import axios from 'axios';
import { getCookie } from 'typescript-cookie';

export const apiInventory = axios.create({
  baseURL: import.meta.env.VITE_URL_BASE_INVENT,
  withCredentials: true,
});

apiInventory.interceptors.request.use(cfg => {
  const token = getCookie('authToken');
  if (token && cfg.headers) {
    // DRF TokenAuthentication espera "Token <key>"
    cfg.headers.Authorization = `Token ${token}`;
  }
  return cfg;
});

