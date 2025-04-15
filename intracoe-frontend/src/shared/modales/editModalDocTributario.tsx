// src/.../EditModal.tsx
import React, { useState, useEffect } from 'react';
import { Dialog } from 'primereact/dialog';
import { Input } from '../forms/input';
import { tipoDocTributarioData } from '../interfaces/interfaces';

interface EditModalDocTributario {
  activity: tipoDocTributarioData;
  visible: boolean;
  setVisible: (v: boolean) => void;
  onSave: () => void; // callback tras guardar para refrescar tabla y cerrar modal
  saveFunction: (
    id: number,
    data: Partial<tipoDocTributarioData>
  ) => Promise<any>;
}

export const EditModalDocTributario: React.FC<EditModalDocTributario> = ({
  activity,
  visible,
  setVisible,
  onSave,
  saveFunction,
}) => {
  const [formData, setFormData] = useState<tipoDocTributarioData>({
    id: activity.id,
    codigo: activity.codigo,
    descripcion: activity.descripcion,
    version: activity.version,
  });

  useEffect(() => {
    setFormData({
      id: activity.id,
      codigo: activity.codigo,
      descripcion: activity.descripcion,
      version: activity.version,
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
        version: formData.version,
      });
      onSave();
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
          version:
          <Input
            name="version"
            value={formData.version}
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
