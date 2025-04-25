
import { removeCookie, setCookie } from 'typescript-cookie';
import { authApi } from '../../../shared/services/auth';

export const login = async (creds: any) => {
  try {
    const resp = await authApi.post('/login/', creds);
    const token = resp.data.token as string;
    setCookie('authToken', token, {
      secure: true,       // solo HTTPS
      sameSite: 'Lax',    // mitiga CSRF
      path: '/',          // disponible en todo el dominio
    });
    return resp.data.user;
  } catch (error: any) {
    console.log(error)
    const msg =
      error.response?.data?.non_field_errors?.[0] ??
      'Error';
    throw new Error(msg);
  }

};

export const logout = async () => {
  try {
    const response = await authApi.post('/logout/');
    removeCookie('authToken');
    return response.data;
  } catch (error: any) {
    console.log(error)
    const msg =
      error.response?.data?.non_field_errors?.[0] ??
      'Error';
    throw new Error(msg);
  }
};

export const ChangePassword = async (data: any) => {
  try {
    const response = await authApi.post('/change-password/', data);
    return response.data
  } catch (error:any) {
    console.log(error)
    const msg =
      error.response?.data?.non_field_errors?.[0] ??
      'Error';
    throw new Error(msg);
  }
}

export const sendCode = async (data:any) => {
  try {
    const response = await authApi.post('/password-reset/', data);
    return response.data
  } catch (error:any) {
    console.log(error)
    const msg =
      error.response?.data?.non_field_errors?.[0] ??
      'Error';
    throw new Error(msg);
  }
}

export const changePassword = async (data:any) => {
  try {
    const response = await authApi.post('/password-reset/confirm/', data);
    return response.data
  } catch (error:any) {
    console.log(error)
    const msg =
      error.response?.data?.non_field_errors?.[0] ??
      'Error';
    throw new Error(msg);
  }
}
