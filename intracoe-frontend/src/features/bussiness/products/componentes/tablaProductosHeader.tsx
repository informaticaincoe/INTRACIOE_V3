import React, { useState } from 'react';

import { LuSearch } from 'react-icons/lu';
import { FaPlus } from 'react-icons/fa';

import { Input } from '../../../../shared/forms/input';
import { useNavigate } from 'react-router';

export const TablaProductosHeader = () => {
  const [formData, setFormData] = useState({
    codigo: '',
  });
  const navigate = useNavigate();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const agregarProducto = () => {
    navigate('/productos/nuevo');
  };

  return (
    <span className="flex items-center justify-between">
      <h1 className="text-lg font-bold">Lista productos</h1>
      <div className="flex gap-5">
        <span className="border-border-color flex w-[30vw] items-center rounded-md border">
          <span className="pl-4">
            <LuSearch />
          </span>
          <Input
            placeholder={'Buscar producto por codigo'}
            name={'codigo'}
            value={formData.codigo}
            onChange={handleChange}
            className="focus:border-ring-0 border-0 focus:border-none focus:ring-0 focus:outline-none active:border-0"
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
