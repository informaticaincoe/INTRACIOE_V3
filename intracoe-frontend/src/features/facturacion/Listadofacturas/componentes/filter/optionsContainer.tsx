import { Divider } from 'primereact/divider';
import React, { useState } from 'react';
import { GoFilter } from 'react-icons/go';
import { FilterContainer } from './filterContainer';
import { AnimatePresence, motion } from 'framer-motion';
import { LuSearch } from 'react-icons/lu';

interface FilterContainerProps {
  total: number;
  setFilters: any;
  filters: any;
}

export const OptionsContainer: React.FC<FilterContainerProps> = ({
  total = 0,
  setFilters,
  filters,
}) => {
  const [showFilters, setShowFilters] = useState(false);
  const [input, setInput] = useState<string>(filters.sello_recepcion);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setInput(value);

    // disparo inmediato del filtro de sello_recepcion:
    setFilters({
      ...filters,
      sello_recepcion: value.trim(),
    });
  };

  return (
    <>
      <div className="flex items-center justify-between">
        <p>{total} resultados</p>
        <span className="flex gap-4">
          <span className="border-border-color flex w-[30vw] items-center rounded-md border">
            <span className="flex pl-4">
              <LuSearch />
            </span>
            <input
              placeholder={'Buscar por sello de recepción...'}
              value={input}
              onChange={handleChange}
              className="focus:border-ring-0 w-full border-0 pl-3 focus:border-none focus:ring-0 focus:outline-none active:border-0"
            />
          </span>
          <button
            className={`flex gap-2 rounded-full px-4 py-2 hover:cursor-pointer ${showFilters ? 'bg-border-color' : 'bg-white'} `}
            onClick={() => setShowFilters(!showFilters)}
          >
            <GoFilter size={24} />
            <span>Filtros</span>
          </button>
        </span>
      </div>
      <Divider />
      <AnimatePresence>
        {showFilters && (
          <motion.div
            key="filterContainer"
            initial={{ opacity: 1, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.3 }}
          >
            <FilterContainer setFilters={setFilters} filters={filters} />
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
};
