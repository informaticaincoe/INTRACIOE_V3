import React, { useEffect, useState } from 'react';
import { getAllCondicionDeOperacion } from '../../../../services/configuracionFactura/configuracionFacturaService';

interface Item {
  name: string;
  value: number;
}

interface SelectCondicionOperacionProps {
  condicionDeOperacion: any;
  setCondicionDeOperacion: any;
}

export const SelectCondicionOperacion: React.FC<
  SelectCondicionOperacionProps
> = ({ condicionDeOperacion, setCondicionDeOperacion }) => {
  const [condicionOperacionApiList, setCondicionOperacionApiList] = useState<
    any[]
  >([]);

  useEffect(() => {
    fetchCondicionDeOperaciones();
  }, []);

  const fetchCondicionDeOperaciones = async () => {
    try {
      const condicionOperaciones = await getAllCondicionDeOperacion();
      console.log('condicionOperaciones', condicionOperaciones);
      setCondicionOperacionApiList(condicionOperaciones);
      setCondicionDeOperacion(condicionOperaciones[0].codigo);
    } catch (error) {
      console.log(error);
    }
  };

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
          {condicionOperacionApiList.map((item) => (
            <button
              key={item.id}
              className={`${condicionDeOperacion === item.codigo ? 'bg-primary-blue text-white' : 'border-primary-blue text-primary-blue border bg-white'} h-14 w-50 rounded-md`} // Cambiar estilo según si está seleccionado
              onClick={() => setCondicionDeOperacion(item.codigo)} //TODO: Enviar id en lugar del nombre
            >
              {item.descripcion}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};
