import { useState } from 'react';
import { Dialog } from 'primereact/dialog';
import React from 'react';
import './antdesignCustom.module.css';
import { Input } from '../../../../../shared/forms/input';
import { createActivity } from '../../services/activitiesServices';

interface NewActivityProps {
  visible: boolean;
  setVisible: any;
}

export const NewActivityForm: React.FC<NewActivityProps> = ({
  visible,
  setVisible,
}) => {
  const [formData, setFormData] = useState({
    codigo: '',
    actividad_economica: '',
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handlerForm = async (e: React.FormEvent) => {
    e.preventDefault();
    const body = {
      codigo: formData.codigo,
      descripcion: formData.actividad_economica,
    };

    console.log('body:', body);
    console.log('tipo:', typeof body);

    try {
      const response = await createActivity(body);
      console.log(response);
      setVisible(false);
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <>
      <Dialog
        header={<p className="px-5 text-xl font-bold">Nueva actividad</p>}
        visible={visible}
        style={{ width: '60vw' }}
        onHide={() => {
          if (!visible) return;
          setVisible(false);
        }}
      >
        <form className="flex flex-col gap-7 px-5">
          <span className="flex flex-col pt-5">
            <label htmlFor="code" className="">
              Codigo:
            </label>
            <Input
              name="codigo"
              placeholder="codigo"
              type="text"
              value={formData.codigo}
              onChange={handleChange}
            />
          </span>
          <span className="flex flex-col pt-5">
            <label htmlFor="code" className="">
              Actividad Economica:
            </label>
            <Input
              name="actividad_economica"
              placeholder="actividad"
              type="text"
              value={formData.actividad_economica}
              onChange={handleChange}
            />
          </span>

          <span className="flex w-full justify-end gap-3">
            <button
              className="bg-primary-blue rounded-md px-6 py-3 text-white hover:cursor-pointer"
              onClick={handlerForm}
            >
              Guardar
            </button>
          </span>
        </form>
      </Dialog>
    </>
  );
};
