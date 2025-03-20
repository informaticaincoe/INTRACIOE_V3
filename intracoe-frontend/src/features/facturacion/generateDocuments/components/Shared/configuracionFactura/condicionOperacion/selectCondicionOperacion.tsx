import React, { useEffect, useState } from 'react';

interface Item {
  name: string;
  value: number;
}


interface SelectCondicionOperacionProps{
  condicionDeOperacion:any,
  setCondicionDeOperacion:any
}

export const SelectCondicionOperacion:React.FC<SelectCondicionOperacionProps> = ({condicionDeOperacion, setCondicionDeOperacion}) => {
  const items: Item[] = [
    { name: 'A contado', value: 1 },
    { name: 'Credito', value: 2 },
    { name: 'Otro', value: 3 },
  ];

  useEffect(()=>{
    
  })

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
              className={`btn ${condicionDeOperacion === item.name ? 'bg-primary-blue text-white' : 'border-primary-blue text-primary-blue border bg-white'} h-14 w-50 rounded-md`} // Cambiar estilo según si está seleccionado
              onClick={() => setCondicionDeOperacion(item.name)} //TODO: Enviar id en lugar del nombre
            >
              {item.name}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};
