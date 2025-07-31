import React, { useEffect, useRef, useState } from 'react';
import { Input } from '../../../../shared/forms/input';
import { ProveedorInterface, ProveedorResultInterface } from '../interfaces/proveedoresInterfaces';
import CustomToast, {
  CustomToastRef,
  ToastSeverity,
} from '../../../../shared/toast/customToast';
import { useNavigate, useParams } from 'react-router';
import {
  addProveedor,
  getProveedoresById,
  updateProveedoresById,
} from '../services/proveedoresServices';
import { FaCheckCircle } from 'react-icons/fa';
import { IoMdCloseCircle } from 'react-icons/io';
import { Title } from '../../../../shared/text/title';

export const ProveedoresNewEdit = () => {
  let params = useParams();
  const toastRef = useRef<CustomToastRef>(null);
  const navigate = useNavigate();
  const [formData, setFormData] = useState<ProveedorResultInterface>({
    id: 0,
    nombre: '',
    ruc_nit: '',
    contacto: null,
    telefono: null,
    email: null,
    direccion: null,
    condiciones_pago: null,
  });

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

  useEffect(() => {
    if (params.id) fetchDataEdit();
  }, []);

  const fetchDataEdit = async () => {
    if (params.id) {
      try {
        const response = await getProveedoresById(params.id);

        if (response && response.id) {
          setFormData(response);
        } else {
          // Si la respuesta no es válida, podemos establecer valores predeterminados
          setFormData({
            id: 0,
            nombre: '',
            ruc_nit: '',
            contacto: null,
            telefono: null,
            email: null,
            direccion: null,
            condiciones_pago: null,
          });
        }

        console.log(response);
      } catch (error) {
        console.log(error);
      }
    }
  };

  const handleChange = (e: any) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSendForm = async () => {
    if (params.id) {
      try {
        const response = await updateProveedoresById(params.id, formData);
        console.log(response);
        handleAccion(
          'success',
          <FaCheckCircle size={38} />,
          'Proveedor actualizado con exito'
        );

        setTimeout(() => {
          navigate('/proveedores/');
        }, 2000);
      } catch (error) {
        handleAccion(
          'error',
          <IoMdCloseCircle size={38} />,
          'Error al actualizar el proveedor'
        );
      }
    } else {
      try {
        const response = await addProveedor(formData);
        console.log(response);
        handleAccion(
          'success',
          <FaCheckCircle size={38} />,
          'proveedor creado con exito'
        );

        setTimeout(() => {
          navigate('/proveedores/');
        }, 2000);
      } catch (error) {
        handleAccion(
          'error',
          <IoMdCloseCircle size={38} />,
          'Error al crear el proveedor'
        );
      }
    }
  };

  return (
    <>
      <CustomToast ref={toastRef} />

      <Title
        text={`${params.id ? ' Editar Proveedor' : 'Nuevo proveedor'} `}
      />
      <div className="mx-[20%] my-10 rounded-md bg-white p-10">
        <div>
          <form action="" className="flex flex-col gap-6 text-start">
            <span>
              <label htmlFor="">Nombre</label>
              <Input
                name="nombre"
                value={formData.nombre}
                onChange={handleChange}
              />
            </span>
            <span>
              <label htmlFor="">NIT o RUC</label>
              <Input
                name="ruc_nit"
                value={formData.ruc_nit}
                onChange={handleChange}
              />
            </span>
            <span>
              <label htmlFor="">Contacto</label>
              <Input
                name="contacto"
                value={formData.contacto ?? ''}
                onChange={handleChange}
              />
            </span>
            <span>
              <label htmlFor="">Telefono</label>
              <Input
                name="telefono"
                value={formData.telefono ?? ''}
                onChange={handleChange}
              />
            </span>
            <span>
              <label htmlFor="">Correo</label>
              <Input
                name="email"
                value={formData.email ?? ''}
                onChange={handleChange}
              />
            </span>
            <span>
              <label htmlFor="">Direccion</label>
              <Input
                name="direccion"
                value={formData.direccion ?? ''}
                onChange={handleChange}
              />
            </span>
            <span>
              <label htmlFor="">Condiciones de pago</label>
              <Input
                name="condiciones_pago"
                value={formData.condiciones_pago ?? ''}
                onChange={handleChange}
              />
            </span>
          </form>
          <div className="flex w-full justify-start pt-5">
            <button
              className="bg-primary-blue rounded-md px-7 py-2 text-white"
              onClick={handleSendForm}
            >
              Guardar
            </button>
          </div>
        </div>
      </div>
    </>
  );
};
