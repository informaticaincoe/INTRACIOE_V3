import React, { useEffect, useState } from 'react';
import { Input } from '../../../../../shared/forms/input';
import { SelectDepartmentComponent } from '../../../../../shared/Select/selectDepartmentComponent';
import { SelectMunicipios } from '../../../../../shared/Select/selectMunicipios';


const StepperContactinfo = (
  {
    formData,
    handleChange,
    handleDepartamento,
    handleMunicipio
  }: {
    formData: any;
    handleChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
    handleDepartamento: (value: string) => void;
    handleMunicipio: (value: string) => void;

  }
) => {
  return (
    <form className="flex flex-col gap-5">
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
        <label htmlFor="direccionComercial">Dirección comercial</label>
        <Input
          name="direccionComercial"
          type="text"
          placeholder=""
          value={formData.direccionComercial}
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
