import { useEffect, useState } from 'react';
import { DepartmentAndMunicipality } from './departmentAndMunicipalityData';
import { Dropdown } from 'primereact/dropdown';

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
    const departmentFetch = DepartmentAndMunicipality.map((element) => ({
      name: element.departamento,
      code: element.codigo,
    }));
    setDepartmentList(departmentFetch);
  }, []);

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
