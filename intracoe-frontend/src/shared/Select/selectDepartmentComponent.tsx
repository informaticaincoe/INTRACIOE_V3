import { useEffect, useState } from 'react';
import { Dropdown } from 'primereact/dropdown';
import { getAllDepartamentos } from '../../features/bussiness/configBussiness/services/ubicacionService';

interface SelectDeparmentInterface {
  onChange: any;
  value: any;
  name: string
}
export const SelectDepartmentComponent: React.FC<SelectDeparmentInterface> = ({
  onChange,
  value,
  name
}) => {
  const [departmentList, setDepartmentList] = useState<any[]>([]);

  useEffect(() => {
    fetchDepartaments();
  }, []);

  const fetchDepartaments = async () => {
    try {
      const response = await getAllDepartamentos();
      const departmentFetch = response.map(
        (element: { id: string; descripcion: any; codigo: any }) => ({
          id: element.id,
          name: element.descripcion,
          code: element.codigo,
        })
      );
      setDepartmentList(departmentFetch);
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <div className="justify-content-center flex">
      <Dropdown
        value={value}
        onChange={(e)=> onChange({ target: { name: name, value: e.value }})}
        options={departmentList}
        optionLabel="name"
        placeholder="Seleccionar departamento"
        className="md:w-14rem font-display w-full"
        filter
      />
    </div>
  );
};
