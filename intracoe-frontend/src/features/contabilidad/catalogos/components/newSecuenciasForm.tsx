import React, { useState, useEffect } from 'react';
import { Dialog } from 'primereact/dialog';
import { Input } from '../../../../shared/forms/input';
import {
  Secuencias,
  SecuenciasDefault,
} from '../../../../shared/interfaces/interfaces';

interface ModalSecuenciasProps {
  visible: boolean;
  setVisible: (v: boolean) => void;
  onSave: () => void;
  createFunction?: (data: Partial<Secuencias>) => Promise<any>;
  saveFunction?: (id: number, data: Partial<Secuencias>) => Promise<any>;
  activity?: Secuencias;
  isEdit: boolean;
}

export const NewModalSecuenciasForm: React.FC<ModalSecuenciasProps> = ({
  visible,
  setVisible,
  onSave,
  createFunction,
  saveFunction,
  activity,
  isEdit,
}) => {
  const [formData, setFormData] = useState<Partial<Secuencias>>(
    activity || SecuenciasDefault
  );

  useEffect(() => {
    if (activity) {
      setFormData(activity);
    } else {
      setFormData(SecuenciasDefault);
    }
  }, [activity]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value, type } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === 'number' ? parseFloat(value) : value,
    }));
  };

  const handlerForm = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const { id, ...rest } = formData;
      if (isEdit && saveFunction && id !== undefined) {
        await saveFunction(id, rest);
      } else if (!isEdit && createFunction) {
        await createFunction(rest);
      }
      onSave();
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <Dialog
      header={isEdit ? 'Editar secuencia' : 'Nueva secuencia'}
      visible={visible}
      style={{ width: '60vw' }}
      onHide={() => setVisible(false)}
    >
      <form className="flex flex-col gap-6 px-5" onSubmit={handlerForm}>
        <label className="flex flex-col">
          Año:
          <Input
            type="number"
            name="anio"
            value={String(formData.anio ?? '')}
            onChange={handleChange}
          />
        </label>

        <label className="flex flex-col">
          Secuencia:
          <Input
            type="number"
            name="secuencia"
            value={String(formData.secuencia ?? '')}
            onChange={handleChange}
          />
        </label>

        <label className="flex flex-col">
          Código DTE:
          <Input
            type="text"
            name="tipo_dte"
            value={formData.tipo_dte ?? ''}
            onChange={handleChange}
          />
        </label>

        <div className="mt-4 flex justify-end">
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
