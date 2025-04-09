import React, { useState } from 'react';

import { LuSearch } from 'react-icons/lu';
import { FaPlus } from 'react-icons/fa';

import { Input } from '../../../../shared/forms/input';
import { useNavigate } from 'react-router';

interface TablaServiciosHeaderProps {
  codigo: string;
  onSearch: (codigo: string) => void;
}


export const TablaServiciosHeader: React.FC<TablaServiciosHeaderProps> = ({ codigo, onSearch }) => {
  const [input, setInput] = useState<string>(codigo);
  const navigate = useNavigate();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInput(e.target.value);
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    // Si el usuario pulsa Enter, ejecuta la búsqueda
    if (e.key === 'Enter') {
      onSearch(input);
    }
  };

  const handleClickSearch = () => {
    onSearch(input);
  };

  const agregarProducto = () => {
    navigate('/productos/nuevo');
  };

  return (
    <span className="flex items-center justify-between">
      <h1 className="text-lg font-bold">Lista Servicios</h1>
      <div className="flex gap-5">
        <span className="border-border-color flex w-[30vw] items-center rounded-md border">
          <span className="pl-4">
            <LuSearch />
          </span>
          <Input
            placeholder="Buscar servicio por código"
            name="codigo"
            value={input}
            onChange={handleChange}
            className="flex-1 border-0 focus:ring-0"
          />
          <button
            onClick={handleClickSearch}
            className="px-3 py-1"
          >
            Buscar
          </button>
        </span>
        <button
          onClick={agregarProducto}
          className="bg-primary-blue flex items-center gap-2 rounded-md px-7 py-3 text-white hover:cursor-pointer"
        >
          <FaPlus size={14} />
          <span>Agregar Servicio</span>
        </button>
      </div>
    </span>
  );
};
