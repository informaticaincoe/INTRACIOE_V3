import React, { useState } from 'react';
import { updateActivity } from '../../services/activitiesServices';
import { Input } from '../../../../../shared/forms/input';
import { Dialog } from 'primereact/dialog';
import { ActivitiesData } from '../../../../../shared/interfaces/interfaces';

interface EditModalProps {
  activity: ActivitiesData;
  onClose: () => void; // Función para cerrar el modal
  onDelete: () => void; // Función para cerrar el modal
  visible: boolean;
  setVisible: any;
}

export const EditModal: React.FC<EditModalProps> = ({
  activity,
  onClose,
  onDelete,
  visible,
  setVisible,
}) => {
  const [formData, setFormData] = useState<ActivitiesData>({
    id: activity.id,
    codigo: activity.codigo,
    descripcion: activity.descripcion,
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    console.log(e.target.value);
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handlerForm = async (e: React.FormEvent) => {
    e.preventDefault();
    const body = {
      codigo: formData.codigo,
      descripcion: formData.descripcion,
    };
    const response = await updateActivity(formData.id, body);
    onDelete();
    onClose();
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
              name="descripcion"
              placeholder="actividad"
              type="text"
              value={formData.descripcion}
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
