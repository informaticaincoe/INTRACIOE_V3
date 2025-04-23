import { useEffect, useState } from 'react';
import { Dropdown } from 'primereact/dropdown';
import { getAllDepartamentos } from '../../features/bussiness/configBussiness/services/ubicacionService';

interface SelectDeparmentInterface {
  setDepartamentoSelect: any;
  departamentoSelect: any;
}
export const SelectDepartmentComponent: React.FC<SelectDeparmentInterface> = ({
  setDepartamentoSelect,
  departamentoSelect,
}) => {
  const [departmentList, setDepartmentList] = useState<any[]>([]);

  useEffect(() => {
    fetchDepartaments();
  }, []);

  useEffect(() => {
    console.log(departamentoSelect);
  }, [departamentoSelect]);

  const fetchDepartaments = async () => {
    try {
      const response = await getAllDepartamentos();
      setDepartmentList(response);
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <div className="justify-content-center flex">
      <Dropdown
        value={departamentoSelect}
        onChange={(e) => setDepartamentoSelect(e.value)}
        options={departmentList}
        optionLabel="descripcion"
        optionValue="id"
        placeholder="Seleccionar departamento"
        className="md:w-14rem font-display w-full"
        filter
      />
    </div>
  );
};
