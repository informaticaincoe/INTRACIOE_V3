import React, { useState } from 'react';

import { LuSearch } from 'react-icons/lu';
import { FaPlus } from 'react-icons/fa';

import { useNavigate } from 'react-router';

interface TablaProductosHeaderProps {
  codigo: string;
  onSearch: (codigo: string) => void;
}

export const TablaProductosHeader: React.FC<TablaProductosHeaderProps> = ({
  codigo,
  onSearch,
}) => {
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
    navigate('/productos/nuevo');
  };

  return (
    <span className="flex items-center justify-between">
      <h1 className="text-lg font-bold">Lista productos</h1>
      <div className="flex gap-5">
        <span className="border-border-color flex w-[30vw] items-center rounded-md border">
          <span className="flex pl-4">
            <LuSearch />
          </span>
          <input
            placeholder={'Buscar producto por codigo o nombre'}
            name="codigo"
            value={input}
            onChange={handleChange}
            onKeyDown={handleKeyPress}
            className="w-full focus:border-ring-0 border-0 pl-3 focus:border-none focus:ring-0 focus:outline-none active:border-0"
          />
        </span>
        <button
          onClick={agregarProducto}
          className="bg-primary-blue flex items-center gap-2 rounded-md px-7 py-3 text-white hover:cursor-pointer"
        >
          <FaPlus size={14} />
          <span>Agregar producto</span>
        </button>
      </div>
    </span>
  );
};
