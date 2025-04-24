import { useEffect, useRef, useState } from 'react';
import { Input } from '../../../shared/forms/input';
import { SendFormButton } from '../../../shared/buttons/sendFormButton';
import { useNavigate } from 'react-router';
import { login, sendCode } from '../services/loginServices';
import CustomToast, { CustomToastRef, ToastSeverity } from '../../../shared/toast/customToast';
import { IoMdCloseCircle } from 'react-icons/io';
import { Dialog } from 'primereact/dialog';
import { InputOtp } from 'primereact/inputotp';

import { RiLockPasswordFill } from "react-icons/ri";

export const LoginForm = () => {
  const navigate = useNavigate(); // Hook para navegar en React Router


  /**************************** Form ****************************/
  const [formData, setFormData] = useState({
    username: '',
    password: '',
  });

  const [errors, setErrors] = useState({
    username: '',
    password: '',
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handlerForm = async (e: React.FormEvent) => {
    e.preventDefault();

    let newErrors = { username: '', password: '' };

    if (!formData.username) {
      newErrors.username = 'Ingrese su usuario';
    }
    if (!formData.password) {
      newErrors.password = 'Ingrese su contraseña';
    }

    setErrors(newErrors);

    if (!newErrors.username && !newErrors.password) {

      try {
        await login(formData)
        navigate('/');
      }
      catch (error: any) {
        console.log(error)
        handleAccion(
          'error',
          <IoMdCloseCircle size={38} />,
          error.toString()
        );
      }
    }
  };
  /*************************************************************/

  /**************************** Toast ****************************/
  const toastRef = useRef<CustomToastRef>(null);

  const handleAccion = (
    severity: ToastSeverity,
    icon: any,
    summary: string
  ) => {
    toastRef.current?.show({
      severity: severity,
      summary: summary,
      icon: icon,
      life: 2000,
    });
  };
  /*************************************************************/

  /* Recuperar contraseña */
  const [email, setEmail] = useState<string>('')
  const [visible, setVisible] = useState<boolean>(false);
  const [codigo, setCodigo] = useState<string | number | null | undefined>(undefined);


  const handleSendCodePassword = async () => {
    setVisible(true)
    try {
      await sendCode({ email: "karen.burgos@grupoincoe.com" })
    } catch (error) {
      console.log(error)
    }
  }

  useEffect(()=>{
    console.log(codigo)
  },[codigo])

  return (
    <>
      <form className="flex w-full flex-col gap-10">
        <span className="flex flex-col gap-5">
          <span className="flex flex-col items-start">
            <label htmlFor="username">Usuario</label>
            <Input
              name="username"
              placeholder="usuario"
              type="text"
              value={formData.username}
              onChange={handleChange}
            />
            {errors.username && (
              <span className="text-sm text-red-500">{errors.username}</span>
            )}
          </span>

          <span className="flex flex-col items-start">
            <label htmlFor="password">Contraseña</label>
            <Input
              name="password"
              placeholder="Contraseña"
              type="password"
              value={formData.password}
              onChange={handleChange}
            />
            {errors.password && (
              <span className="text-sm text-red-500">{errors.password}</span>
            )}
          </span>
          <p className='text-blue underline text-end' onClick={handleSendCodePassword}>¿Olvidaste tu contraseña?</p>

        </span>
        <SendFormButton className='bg-primary-blue text-white' text="Ingresar" onClick={handlerForm} />
        <CustomToast ref={toastRef} />
      </form>
      {
        visible &&
        <Dialog visible={visible} style={{ width: '50vw' }} onHide={() => { if (!visible) return; setVisible(false); }}>
          <div>
            <RiLockPasswordFill size={100} className='text-center w-full pb-5' />
            <p className='text-xl font-bold text-center'>Codigo de recuperación</p>
            <label className="m-0 text-center">
              Codigo de recuperación enviado al correo:
              <span className='italic'> karen.burgos@grupoincoe.com</span>
            </label>
            <div className='pt-5 flex flex-col justify-center items-center'>
              <label htmlFor="codigo">Codigo de verificacion:</label>
              <InputOtp name="codigo" value={codigo} onChange={(e) => setCodigo(e.value)} integerOnly length={6} style={{ padding: '3% 0' }} />
            </div>
          </div>
        </Dialog>
      }
    </>
  );
};
