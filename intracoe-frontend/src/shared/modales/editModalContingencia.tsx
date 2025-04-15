// src/.../EditModal.tsx
import React, { useState, useEffect } from 'react';
import { Dialog } from 'primereact/dialog';
import { Input } from '../forms/input';
import { contingenciaData } from '../interfaces/interfaces';

interface EditModalContingenciaProps {
  activity: contingenciaData;
  visible: boolean;
  setVisible: (v: boolean) => void;
  onSave: () => void; // callback tras guardar para refrescar tabla y cerrar modal
  saveFunction: (id: number, data: Partial<contingenciaData>) => Promise<any>;
}

export const EditModalContingencia: React.FC<EditModalContingenciaProps> = ({
  activity,
  visible,
  setVisible,
  onSave,
  saveFunction,
}) => {
  const [formData, setFormData] = useState<contingenciaData>({
    id: activity.id,
    codigo: activity.codigo,
    descripcion: activity.descripcion,
    motivo_contingencia: activity.motivo_contingencia,
  });

  useEffect(() => {
    setFormData({
      id: activity.id,
      codigo: activity.codigo,
      descripcion: activity.descripcion,
      motivo_contingencia: activity.motivo_contingencia,
    });
  }, [activity]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handlerForm = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      // Aquí uso la función dinámica que viene por props
      await saveFunction(formData.id, {
        codigo: formData.codigo,
        descripcion: formData.descripcion,
        motivo_contingencia: formData.motivo_contingencia,
      });
      onSave();
      setVisible(false);
    } catch (err) {
      console.error(err);
      // mostrar toast de error si quieres
    }
  };

  return (
    <Dialog
      header="Editar registro"
      visible={visible}
      style={{ width: '60vw' }}
      onHide={() => setVisible(false)}
    >
      <form className="flex flex-col gap-7 px-5" onSubmit={handlerForm}>
        <label>
          Código:
          <Input
            name="codigo"
            value={formData.codigo}
            onChange={handleChange}
          />
        </label>
        <label>
          Descripción:
          <Input
            name="descripcion"
            value={formData.descripcion}
            onChange={handleChange}
          />
        </label>
        <label>
          Motivo contingencia:
          <Input
            name="motivo_contingencia"
            value={formData.motivo_contingencia}
            onChange={handleChange}
          />
        </label>
        <div className="flex justify-end gap-3">
          <button
            type="submit"
            className="bg-primary-blue rounded px-6 py-2 text-white"
          >
            Guardar
          </button>
        </div>
      </form>
    </Dialog>
  );
};
