import React, { useEffect, useState } from 'react';
import { DepartmentAndMunicipality } from './departmentAndMunicipalityData';
import { Dropdown } from 'primereact/dropdown';

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
  const [municipalities, setMunicipalities] = useState<any[]>([]);

  useEffect(() => {
    console.log(department);
    if (department) {
      // Filtramos los municipios según el departamento seleccionado
      const departmentData = DepartmentAndMunicipality.find(
        (d) => d.codigo === department.code
      );

      if (departmentData) {
        console.log(departmentData.municipios);

        const municipalityListAux = departmentData.municipios.map(
          (element) => ({
            name: element.municipio,
            code: element.codigo,
          })
        );
        setMunicipalities(municipalityListAux);
      }
    }
  }, [department, department]); // Se ejecuta cuando cambia el departamento seleccionado

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
