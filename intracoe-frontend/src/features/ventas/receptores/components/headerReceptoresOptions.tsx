import React, { useState } from 'react';
import { LuSearch } from 'react-icons/lu';
import { FaPlus } from 'react-icons/fa';

import { useNavigate } from 'react-router';

interface HeaderReceptoresOptionsProps {
  codigo: string;
  onSearch: (codigo: string) => void;
}

export const HeaderReceptoresOptions: React.FC<
  HeaderReceptoresOptionsProps
> = ({ codigo, onSearch }) => {
  const [input, setInput] = useState<string>(codigo);
  const navigate = useNavigate();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInput(e.target.value);
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    console.log(e.target);
    // Si el usuario pulsa Enter, ejecuta la búsqueda
    onSearch(input);
  };

  const agregarProducto = () => {
    navigate('/receptor/nuevo');
  };

  return (
    <span className="flex items-center justify-between">
      <h1 className="text-lg font-bold">Lista receptores</h1>
      <div className="flex gap-5">
        <span className="border-border-color flex w-[30vw] items-center gap-2 rounded-md border">
          <span className="pl-5">
            <LuSearch />
          </span>
          <input
            placeholder={
              'Buscar producto por nombre o numero de identificacion'
            }
            name="filtro"
            value={input}
            onChange={handleChange}
            onKeyDown={handleKeyPress}
            className="focus:border-ring-0 w-full border-0 focus:border-none focus:ring-0 focus:outline-none active:border-0"
          />
        </span>
        <button
          onClick={agregarProducto}
          className="bg-primary-blue flex items-center gap-2 rounded-md px-7 py-3 text-white hover:cursor-pointer"
        >
          <FaPlus size={14} />
          <span>Agregar Receptor</span>
        </button>
      </div>
    </span>
  );
};
