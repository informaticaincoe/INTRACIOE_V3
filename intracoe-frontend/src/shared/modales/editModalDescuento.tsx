import React, { useState, useEffect } from 'react';
import { Dialog } from 'primereact/dialog';
import { Input } from '../forms/input';
import { RadioButton, RadioButtonChangeEvent } from 'primereact/radiobutton';
import { Descuento } from '../interfaces/interfaces';

interface EditModalDescuentoProps {
  activity: Descuento;
  visible: boolean;
  setVisible: (v: boolean) => void;
  onSave: () => void;
  saveFunction: (id: number, data: Partial<Descuento>) => Promise<any>;
}

export const EditModalDescuento: React.FC<EditModalDescuentoProps> = ({
  activity,
  visible,
  setVisible,
  onSave,
  saveFunction,
}) => {
  // formData.estdo es boolean
  const [formData, setFormData] = useState<Descuento>(activity);

  useEffect(() => {
    setFormData(activity);
  }, [activity]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value, type } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === 'number' ? parseFloat(value) : value,
    }));
  };

  // Handler para el radio booleano
  const handleEstadoChange = (e: RadioButtonChangeEvent) => {
    setFormData((prev) => ({
      ...prev,
      estdo: e.value as boolean,
    }));
  };

  const handlerForm = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const { id, ...rest } = formData;
      await saveFunction(id, rest);
      onSave();
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <Dialog
      header="Editar Descuento"
      visible={visible}
      style={{ width: '60vw' }}
      onHide={() => setVisible(false)}
    >
      <form className="flex flex-col gap-6 px-5" onSubmit={handlerForm}>
        <label className="flex flex-col">
          Porcentaje:
          <Input
            type="number"
            name="porcentaje"
            value={String(formData.porcentaje)}
            onChange={handleChange}
          />
        </label>

        <label className="flex flex-col">
          Descripción:
          <Input
            name="descripcion"
            value={formData.descripcion}
            onChange={handleChange}
          />
        </label>

        <label className="flex flex-col">
          Fecha de inicio:
          <Input
            type="date"
            name="fecha_inicio"
            value={formData.fecha_inicio}
            onChange={handleChange}
          />
        </label>

        <label className="flex flex-col">
          Fecha fin:
          <Input
            type="date"
            name="fecha_fin"
            value={formData.fecha_fin}
            onChange={handleChange}
          />
        </label>

        <label className="flex flex-col">
          Estado:
          <div className="flex gap-8 pt-2">
            <div className="flex items-center">
              <RadioButton
                inputId="estado-true"
                name="estdo"
                value={true} // boolean
                onChange={handleEstadoChange}
                checked={formData.estdo === true}
              />
              <label htmlFor="estado-true" className="ml-2">
                Activo
              </label>
            </div>
            <div className="flex items-center">
              <RadioButton
                inputId="estado-false"
                name="estdo"
                value={false} // boolean
                onChange={handleEstadoChange}
                checked={formData.estdo === false}
              />
              <label htmlFor="estado-false" className="ml-2">
                Inactivo
              </label>
            </div>
          </div>
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
