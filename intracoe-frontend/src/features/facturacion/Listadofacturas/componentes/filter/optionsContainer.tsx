import { Divider } from 'primereact/divider';
import React, { useState } from 'react';
import { GoFilter } from 'react-icons/go';
import { FilterContainer } from './filterContainer';
import { AnimatePresence, motion } from 'framer-motion';

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

  return (
    <>
      <div className="flex items-center justify-between">
        <p>{total} resultados</p>
        <button
          className={`flex gap-2 rounded-full px-4 py-2 hover:cursor-pointer ${showFilters ? 'bg-border-color' : 'bg-white'} `}
          onClick={() => setShowFilters(!showFilters)}
        >
          <GoFilter size={24} />
          <span>Filtros</span>
        </button>
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
