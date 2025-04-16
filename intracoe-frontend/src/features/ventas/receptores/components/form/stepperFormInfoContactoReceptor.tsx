import React, { useEffect, useState } from 'react';
import { ReceptorRequestInterface } from '../../../../../shared/interfaces/interfaces';
import { Input } from '../../../../../shared/forms/input';
import { SelectDepartmentComponent } from '../../../../../shared/Select/selectDepartmentComponent';
import { SelectMunicipios } from '../../../../../shared/Select/selectMunicipios';
import { getMunicipiosById } from '../../../../bussiness/configBussiness/services/ubicacionService';

interface StepperFormInfoContactoReceptorProps {
  formData: ReceptorRequestInterface;
  handleChange: any;
}

export const StepperFormInfoContactoReceptor: React.FC<
  StepperFormInfoContactoReceptorProps
> = ({ formData, handleChange }) => {
  const [departamentoSelect, setDepartamentoSelect] = useState<string>();

  useEffect(() => {
    if (formData.municipio) fetchDepartamento(); //obtener departamento por medio del municipio cuando se vaya a editar
  }, []);

  const fetchDepartamento = async () => {
    try {
      const response = await getMunicipiosById(formData.municipio);
      console.log('Departamento', response);
      setDepartamentoSelect(response.departamento);
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <div>
      <span>
        <label htmlFor="departamento">Departamentos</label>
        <SelectDepartmentComponent
          setDepartamentoSelect={setDepartamentoSelect}
          departamentoSelect={departamentoSelect}
        />
      </span>
      <span>
        <label htmlFor="municipio">Municipio</label>
        <SelectMunicipios
          onChange={handleChange}
          department={departamentoSelect}
          value={formData.municipio}
          name={'municipio'}
        />
      </span>
      <span>
        <label htmlFor="direccion">Direccion</label>
        <Input
          onChange={handleChange}
          value={formData.direccion}
          name={'direccion'}
        />
      </span>
      <span>
        <label htmlFor="telefono">Telefono</label>
        <Input
          onChange={handleChange}
          value={formData.telefono}
          name={'telefono'}
        />
      </span>
      <span>
        <label htmlFor="correo">Correo</label>
        <Input
          onChange={handleChange}
          value={formData.correo}
          name={'correo'}
        />
      </span>
    </div>
  );
};
