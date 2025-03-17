import { useEffect, useState } from 'react';
import { Dropdown } from 'primereact/dropdown';
import { getAllDepartamentos } from '../../features/bussiness/configBussiness/services/ubicacionService';

interface SelectDeparmentInterface {
  department: any;
  setDepartment: any;
}
export const SelectDepartmentComponent: React.FC<SelectDeparmentInterface> = ({
  department,
  setDepartment,
}) => {
  const [departmentList, setDepartmentList] = useState<any[]>([]);

  useEffect(() => {
    fetchDepartaments();
  }, []);

  const fetchDepartaments = async () => {
    try {
      const response = await getAllDepartamentos();

      console.log(response);
      const departmentFetch = response.map(
        (element: { id: string; descripcion: any; codigo: any }) => ({
          id: element.id,
          name: element.descripcion,
          code: element.codigo,
        })
      );
      console.log('departmentFetch', departmentFetch);
      setDepartmentList(departmentFetch);
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <div className="justify-content-center flex">
      <Dropdown
        value={department}
        onChange={(e) => setDepartment(e.value)}
        options={departmentList}
        optionLabel="name"
        placeholder="Seleccionar tipo de establecimiento"
        className="md:w-14rem font-display w-full"
        filter
      />
    </div>
  );
};
