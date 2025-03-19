import React, { useState } from 'react';
import { Input } from '../../../../../../shared/forms/input';

interface Item {
  name: string;
  value: number;
}

export const SelectCondicionOperacion = () => {
  const [value, setValue] = useState<string>('A contado');
  const items: Item[] = [
    { name: 'A contado', value: 1 },
    { name: 'Credito', value: 2 },
    { name: 'Otro', value: 3 },
  ];

  const [formData, setFormData] = useState({
    otraOperacion: '',
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  return (
    <div className="flex flex-col gap-1">
      <label htmlFor="condicion" className="text-start opacity-70">
        Condición de operación
      </label>
      <div className="flex flex-col gap-8">
        <div className="flex gap-10">
          {items.map((item) => (
            <button
              key={item.value}
              className={`btn ${value === item.name ? 'bg-primary-blue text-white' : 'border-primary-blue text-primary-blue border bg-white'} h-14 w-50 rounded-md`} // Cambiar estilo según si está seleccionado
              onClick={() => setValue(item.name)} //TODO: Enviar id en lugar del nombre
            >
              {item.name}
            </button>
          ))}
        </div>
        {value == 'Otro' && (
          <div className="gap-1 text-start">
            <label htmlFor="otraOperacion" className="opacity-70">
              Descripción:
            </label>
            <Input
              name="otraOperacion"
              placeholder="Expecifique la condición"
              type="text"
              value={formData.otraOperacion}
              onChange={handleChange}
            />
          </div>
        )}
      </div>
    </div>
  );
};
