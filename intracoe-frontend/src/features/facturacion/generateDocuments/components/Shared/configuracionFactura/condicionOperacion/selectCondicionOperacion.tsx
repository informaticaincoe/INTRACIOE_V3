import React, { useEffect, useState } from 'react';

interface Item {
  name: string;
  value: number;
}

interface SelectCondicionOperacionProps {
  selectedCondicionDeOperacion: any;
  setSelectedCondicionDeOperacion: any;
  condicionesOperacionList: any;
}

export const SelectCondicionOperacion: React.FC<
  SelectCondicionOperacionProps
> = ({
  selectedCondicionDeOperacion,
  setSelectedCondicionDeOperacion,
  condicionesOperacionList,
}) => {
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
          {condicionesOperacionList &&
            condicionesOperacionList.map((item: any) => (
              <button
                key={item.id}
                className={`${selectedCondicionDeOperacion === item.codigo ? 'bg-primary-blue text-white' : 'border-primary-blue text-primary-blue border bg-white'} h-14 w-50 rounded-md`} // Cambiar estilo según si está seleccionado
                onClick={() => setSelectedCondicionDeOperacion(item.codigo)} //TODO: Enviar id en lugar del nombre
              >
                {item.descripcion}
              </button>
            ))}
        </div>
      </div>
    </div>
  );
};
