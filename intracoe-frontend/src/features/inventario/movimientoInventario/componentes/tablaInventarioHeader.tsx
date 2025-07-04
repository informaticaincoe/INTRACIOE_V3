import React, { useState } from 'react';
import { FaPlus } from 'react-icons/fa6';
import { LuSearch } from 'react-icons/lu';
import { useNavigate } from 'react-router';

interface TablaProductosHeaderProps {
  codigo: string;
  onSearch: (codigo: string) => void;
  results: number;
}

export const TablaInventarioHeader: React.FC<TablaProductosHeaderProps> = ({
  codigo,
  onSearch,
  results,
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

  const agregarMovimiento = () => {
    navigate('/movimiento-inventario/nuevo');
  };

  return (
    <span className="flex items-center justify-between">
      <span className="text-start">
        <h1 className="text-lg font-bold">Lista movimiento de inventario</h1>
        <h1 className="">{results} Resultados</h1>
      </span>
      <div className="flex gap-5">
        <span className="border-border-color flex w-[30vw] items-center rounded-md border">
          <span className="flex pl-4">
            <LuSearch />
          </span>
          <input
            name="codigo"
            value={input}
            onChange={handleChange}
            onKeyDown={handleKeyPress}
            className="focus:border-ring-0 w-full border-0 pl-3 focus:border-none focus:ring-0 focus:outline-none active:border-0"
          />
        </span>
        <button
          onClick={agregarMovimiento}
          className="bg-primary-blue flex items-center gap-2 rounded-md px-7 py-3 text-white hover:cursor-pointer"
        >
          <FaPlus size={14} />
          <span>Agregar movimiento</span>
        </button>
      </div>
    </span>
  );
};
