import React, { useEffect, useState } from 'react';
import { DepartmentAndMunicipality } from './departmentAndMunicipalityData';
import { Dropdown } from 'primereact/dropdown';
import { getMunicipiosByDepartamentos } from '../../features/bussiness/configBussiness/services/ubicacionService';

interface SelectMunicipioInterface {
  department: any; // Recibe el departamento seleccionado
  municipio: any;
  setMunicipio: React.Dispatch<React.SetStateAction<any>>; // Para actualizar el municipio seleccionado
}

export const SelectMunicipios: React.FC<SelectMunicipioInterface> = ({
  department,
  municipio,
  setMunicipio,
}) => {
  const [municipalities, setMunicipalities] = useState<[]>([]);

  useEffect(() => {
    fetchMunicipalitiesByDepartment();
  }, [department, department]);

  const fetchMunicipalitiesByDepartment = async () => {
    try {
      if (department.id != '') {
        console.log(department.id);
        const response = await getMunicipiosByDepartamentos(department.id);
        const municipalityList = response.map(
          (element: { id: string; descripcion: any; codigo: any }) => ({
            id: element.id,
            name: element.descripcion,
            code: element.codigo,
          })
        );
        console.log(municipalityList);
        setMunicipalities(municipalityList);
      }
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <div className="justify-content-center flex">
      <Dropdown
        value={municipio}
        onChange={(e) => setMunicipio(e.value)}
        options={municipalities}
        optionLabel="name"
        placeholder="Seleccionar tipo de establecimiento"
        className="md:w-14rem font-display w-full"
        filter
      />
    </div>
  );
};
