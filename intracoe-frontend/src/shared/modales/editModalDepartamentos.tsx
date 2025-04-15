// src/.../EditModal.tsx
import React, { useState, useEffect } from 'react';
import { Dialog } from 'primereact/dialog';
import { Input } from '../forms/input';
import { DepartamentoCatalogo, PaisCatalogo } from '../interfaces/interfaces';
import { getAllPaises } from '../catalogos/services/catalogosServices';
import { Dropdown } from 'primereact/dropdown';

interface EditModalDocTributario {
  activity: DepartamentoCatalogo;
  visible: boolean;
  setVisible: (v: boolean) => void;
  onSave: () => void; // callback tras guardar para refrescar tabla y cerrar modal
  saveFunction: (
    id: string,
    data: Partial<DepartamentoCatalogo>
  ) => Promise<any>;
}

export const EditModalDepartamento: React.FC<EditModalDocTributario> = ({
  activity,
  visible,
  setVisible,
  onSave,
  saveFunction,
}) => {
  const [paisesList, setPaisesList] = useState<PaisCatalogo[]>([]);
  const [paisSelect, setPaisSelect] = useState<PaisCatalogo>();

  const [formData, setFormData] = useState<DepartamentoCatalogo>({
    id: activity.id,
    codigo: activity.codigo,
    descripcion: activity.descripcion,
    pais: activity.pais,
  });

  useEffect(() => {
    fetchPaises;
  }, []);

  const fetchPaises = async () => {
    try {
      const response = await getAllPaises();
      console.log('pais', response);
      setPaisesList(response);
    } catch (error) {
      console.log(error);
    }
  };

  useEffect(() => {
    setFormData({
      id: activity.id,
      codigo: activity.codigo,
      descripcion: activity.descripcion,
      pais: activity.pais,
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
        pais: formData.pais,
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
        <span>
          <label>Código:</label>
          <Input
            name="codigo"
            value={formData.codigo}
            onChange={handleChange}
          />
        </span>

        <span>
          <label>Descripción:</label>
          <Input
            name="descripcion"
            value={formData.descripcion}
            onChange={handleChange}
          />
        </span>
        <span>
          <label htmlFor="pais">Pais:</label>
          <Dropdown
            value={paisSelect}
            onChange={(e) => setPaisSelect(e.value)}
            options={paisesList}
            placeholder="Seleccionar pais..."
            optionValue="codigo"
            className="w-full"
            checkmark={true}
          />
        </span>
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
