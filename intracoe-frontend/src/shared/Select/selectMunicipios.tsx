import React, { useEffect, useState } from 'react';
import { Dropdown } from 'primereact/dropdown';
import { getMunicipiosByDepartamentos } from '../../features/bussiness/configBussiness/services/ubicacionService';

interface SelectMunicipiosInterface {
  name: string;
  department: any; // Recibe el departamento seleccionado
  value: any;
  onChange: React.Dispatch<React.SetStateAction<any>>; // Para actualizar el value seleccionado
}

export const SelectMunicipios: React.FC<SelectMunicipiosInterface> = ({
  name,
  department,
  value,
  onChange,
}) => {
  const [municipalities, setMunicipalities] = useState<[]>([]);

  useEffect(() => {
    fetchMunicipalitiesByDepartment();
    console.log('municipio departamento', department);
  }, []);

  useEffect(() => {
    fetchMunicipalitiesByDepartment();
  }, [department]);

  const fetchMunicipalitiesByDepartment = async () => {
    try {
      if (department) {
        const response = await getMunicipiosByDepartamentos(department);
        setMunicipalities(response);
        console.log(response);
      }
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <div className="justify-content-center flex">
      <Dropdown
        name={name}
        value={value}
        onChange={(e) => onChange({ target: { name: name, value: e.value } })}
        options={municipalities}
        optionLabel="descripcion"
        optionValue="id"
        placeholder="Seleccionar tipo de establecimiento"
        className="md:w-14rem font-display w-full"
        filter
      />
    </div>
  );
};
