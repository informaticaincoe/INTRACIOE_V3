import React from 'react';
import { Input } from '../../../../../shared/forms/input';
import { SelectDepartmentComponent } from '../../../../../shared/Select/selectDepartmentComponent';
import { SelectMunicipios } from '../../../../../shared/Select/selectMunicipios';
import { Departamento, Municipio } from '../../interfaces/empresaInterfaces';

const StepperContactinfo = ({
  formData,
  handleChange,
  handleDepartamento,
  handleMunicipio,
  errores,
}: {
  formData: any;
  handleChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  handleDepartamento: (value: Departamento) => void;
  handleMunicipio: (value: Municipio) => void;
  errores: any;
}) => {
  return (
    <form className="flex flex-col gap-5">
      <span className="w-full text-start">
        <span className="text-red pr-1">*</span>

        <label htmlFor="departamento" className="">
          Dirección comercial
        </label>
        <Input
          name="direccion_comercial"
          type="text"
          placeholder=""
          value={formData.direccion_comercial}
          onChange={handleChange}
        />
        {errores.direccion_comercial && (
          <span className="text-sm text-red-500">
            {errores.direccion_comercial}
          </span>
        )}
      </span>
      <span className="w-full text-start">
        <label htmlFor="departamento" className="">
          Departamento
        </label>
        <SelectDepartmentComponent
          department={formData.departamento}
          setDepartment={handleDepartamento}
        />
      </span>
      <span className="w-full text-start">
        <label htmlFor="municipio">Municipio</label>
        <SelectMunicipios
          department={formData.departamento}
          municipio={formData.municipio}
          setMunicipio={handleMunicipio}
        />
      </span>
      <span className="w-full text-start">
        <label htmlFor="direccion_comercial">Correo</label>
        <Input
          name="email"
          type="text"
          placeholder=""
          value={formData.email}
          onChange={handleChange}
        />
      </span>
      <span className="w-full text-start">
        <label htmlFor="telefono">Telefono</label>
        <Input
          name="telefono"
          type="text"
          placeholder=""
          value={formData.telefono}
          onChange={handleChange}
        />
      </span>
    </form>
  );
};

export default StepperContactinfo;
