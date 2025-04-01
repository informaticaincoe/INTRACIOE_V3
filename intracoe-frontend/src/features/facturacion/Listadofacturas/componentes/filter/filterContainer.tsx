import { Divider } from 'primereact/divider';
import React from 'react';
import { GoFilter } from 'react-icons/go';

interface FilterContainerProps {
  total: number;
}

export const FilterContainer: React.FC<FilterContainerProps> = ({
  total = 0,
}) => {
  return (
    <>
      <div className="flex items-center justify-between">
        <p>{total} resultados</p>
        <div className="flex gap-2 rounded-full px-4 py-2">
          <GoFilter size={24} />
          <span>Filtros</span>
        </div>
      </div>
      <Divider />
    </>
  );
};
