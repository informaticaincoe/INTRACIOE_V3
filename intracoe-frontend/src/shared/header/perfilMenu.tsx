import { Sidebar } from 'primereact/sidebar';
import defaultPerfil from '../../assets/grupo_incoe_logo.png';
import { useRef, useState } from 'react';
import { password, Perfil } from '../interfaces/interfaces';
import banner from '../../assets/banner.png';
import { Divider } from 'primereact/divider';
import { Dialog } from 'primereact/dialog';
import { Input } from '../forms/input';
/* icons */
import { RiLockPasswordLine } from 'react-icons/ri';
import { IoIosLogOut } from 'react-icons/io';
import { MdPerson } from 'react-icons/md';
import { HiOutlineStatusOnline } from 'react-icons/hi';
import { FaCircleCheck, FaRegClock } from 'react-icons/fa6';
import { TbLogout } from "react-icons/tb";

import { EditableField } from './editableFiedl';
import {
  ChangePassword,
  logout,
} from '../../features/login/services/loginServices';
import { useNavigate } from 'react-router';
import CustomToast, {
  CustomToastRef,
  ToastSeverity,
} from '../toast/customToast';

interface PerfilMenuProps {
  visible: boolean;
  setVisible: any;
}

export const PerfilMenu: React.FC<PerfilMenuProps> = ({
  visible,
  setVisible,
}) => {
  const navigate = useNavigate();
  const [visibleChangePassword, setVisibleChangePassword] = useState(false);
  const [formData, setFormData] = useState<Perfil>({
    usuario: 'admin',
    correo: 'admin@email.com',
  });
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

  const [firstName, setFirstName] = useState('Nombre');
  const [lastName, setLastName] = useState('Apellido');
  const [passwordConfirm, setPasswordConfirm] = useState<string>('');

  const [formDataPasswordChange, setFormDataPasswordChange] =
    useState<password>({
      old_password: '',
      new_password: '',
    });

  const [errors, setErrors] = useState<{
    old_password?: string;
    new_password?: string;
    confirmPassword?: string;
    errorCambiarContra?: string;
  }>({});

  const [passwordError, setPasswordError] = useState<string>('');

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleChangePassword = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormDataPasswordChange({
      ...formDataPasswordChange,
      [e.target.name]: e.target.value,
    });
    // limpiar error al escribir
    setPasswordError('');
  };

  const handleConfirmChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setPasswordConfirm(e.target.value);
    setErrors((prev) => ({ ...prev, confirmPassword: undefined }));
  };

  const logoutHandler = async () => {
    try {
      const response = await logout();
      console.log(response);
      navigate('/login');
    } catch (error) {
      console.log(error);
    }
  };

  const onSubmitPassword = async () => {
    const { old_password, new_password } = formDataPasswordChange;
    const newErrors: typeof errors = {};

    if (!old_password)
      newErrors.old_password = 'Ingresa tu contraseña anterior.';
    if (!new_password) newErrors.new_password = 'Ingresa la nueva contraseña.';
    if (!passwordConfirm)
      newErrors.confirmPassword = 'Confirma tu nueva contraseña.';
    if (new_password && passwordConfirm && new_password !== passwordConfirm) {
      newErrors.confirmPassword = 'La confirmación no coincide.';
    }

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    try {
      await ChangePassword(formDataPasswordChange);
      // Cerrar diálogo y limpiar estados
      setVisibleChangePassword(false);
      setFormDataPasswordChange({ old_password: '', new_password: '' });
      setPasswordConfirm('');
      setErrors({});
      handleAccion(
        'success',
        <FaCircleCheck size={38} />,
        'contraseña actualizada con exito'
      );
    } catch (error) {
      console.log(error);
      setErrors({ errorCambiarContra: 'Contraseña anterior incorrecta' });
    }
  };

  return (
    <>
      <Sidebar
        position="right"
        visible={visible}
        onHide={() => setVisible(false)}
        style={{ width: '20vw' }}
      >
        <div className="flex h-full flex-col justify-between">
          <div>
            <div className="relative mb-10 flex w-full flex-col items-center">
              {/* Banner de fondo */}
              <img src={banner} className="h-30 w-full bg-blue-200" />

              {/* Imagen de perfil */}
              <div className="absolute top-10">
                <img
                  src={defaultPerfil}
                  alt="perfil"
                  className="h-30 w-30 rounded-full border-4 border-white object-cover shadow-md"
                />
              </div>
            </div>

            {/* Sección Usuario */}
            <div className="flex flex-col px-5 py-3">
              {/* Usuario */}
              <EditableField
                value={formData.usuario}
                onSave={(val) => setFormData({ ...formData, usuario: val })}
                labelClass="text-lg font-bold"
              />

              {/* Correo */}
              <EditableField
                value={formData.correo}
                onSave={(val) => setFormData({ ...formData, correo: val })}
              />
            </div>

            <div className="mt-15 space-y-10 px-7 text-sm text-gray-700">
              {/* Perfil */}
              <div>
                <span className="flex items-center gap-2">
                  <MdPerson size={20} className="opacity-60" />
                  <p className="font-medium text-gray-800">Perfil</p>
                </span>
                <Divider
                  pt={{
                    root: {
                      style: {
                        margin: '4% 0',
                        padding: 0,
                      },
                    },
                  }}
                />

                <div className="space-y-1 px-7 text-gray-600">
                  <p>Nombre: {firstName}</p>
                  <p>Apellido: {lastName}</p>
                </div>
              </div>
              {/* Estado */}
              <div>
                <span className="flex items-center gap-2">
                  <HiOutlineStatusOnline size={22} className="opacity-70" />
                  <p className="font-medium text-gray-800">Estado</p>
                </span>
                <Divider
                  pt={{
                    root: {
                      style: {
                        margin: '4% 0',
                        padding: 0,
                      },
                    },
                  }}
                />
                <div className="px-7 font-medium text-green-600">● Activo</div>
              </div>

              {/* Última conexión */}
              <div>
                <span className="flex items-center gap-2">
                  <FaRegClock size={18} className="opacity-70" />
                  <p className="font-medium text-gray-800">Última conexión</p>
                </span>
                <Divider
                  pt={{
                    root: {
                      style: {
                        margin: '4% 0',
                        padding: 0,
                      },
                    },
                  }}
                />
                <div className="px-7 text-gray-600">2025-04-08 15:12:23</div>
              </div>
            </div>
          </div>

          {/* Cambio de Contraseña */}
          <div className="px-7 pb-5">
            <span
              className="flex items-center gap-2 hover:cursor-pointer"
              onClick={() => setVisibleChangePassword(true)}
            >
              <TbLogout size={18}/>
              <p className="">Cambiar contraseña</p>
            </span>
            <Divider />
            <button className="flex items-center gap-2 hover:cursor-pointer" onClick={logoutHandler}>
              <IoIosLogOut size={20} />
              <p className="">Cerrar sesión</p>
            </button>
          </div>
        </div>
        <CustomToast ref={toastRef} />
      </Sidebar>
      {visibleChangePassword && (
        <Dialog
          header="Cambiar contraseña"
          visible={visibleChangePassword}
          modal
          style={{ width: '35vw' }}
          onHide={() => setVisibleChangePassword(false)}
        >
          {errors.errorCambiarContra && (
            <small className="px-4 text-red-500">
              {errors.errorCambiarContra}
            </small>
          )}
          <div className="flex flex-col gap-6 px-5 py-4">
            <div className="flex flex-col gap-4">
              <div>
                <p>Contraseña anterior:</p>
                <Input
                  name="old_password"
                  type="password"
                  value={formDataPasswordChange.old_password}
                  onChange={handleChangePassword}
                />
                {errors.old_password && (
                  <small className="text-red-500">{errors.old_password}</small>
                )}
              </div>

              <div>
                <p>Nueva contraseña:</p>
                <Input
                  name="new_password"
                  type="password"
                  value={formDataPasswordChange.new_password}
                  onChange={handleChangePassword}
                />
                {errors.new_password && (
                  <small className="text-red-500">{errors.new_password}</small>
                )}
              </div>

              <div>
                <p>Confirmar nueva contraseña:</p>
                <Input
                  name="confirmPassword"
                  type="password"
                  value={passwordConfirm}
                  onChange={handleConfirmChange}
                />
                {errors.confirmPassword && (
                  <small className="text-red-500">
                    {errors.confirmPassword}
                  </small>
                )}
              </div>
            </div>

            <button
              className="bg-primary-blue rounded-md py-3 text-white"
              onClick={onSubmitPassword}
            >
              Cambiar contraseña
            </button>
          </div>
        </Dialog>
      )}
    </>
  );
};
