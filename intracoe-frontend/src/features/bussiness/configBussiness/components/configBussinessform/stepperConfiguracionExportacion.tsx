import { useEffect, useState } from 'react';
import { RequestEmpresa } from '../../../../../shared/interfaces/interfaces';
import { Input } from '../../../../../shared/forms/input';

interface StepperConfiguracionExportacionProp {
  formData: RequestEmpresa;
  handleChange: any;
}

export const StepperConfiguracionExportacion: React.FC<StepperConfiguracionExportacionProp> = ({
  formData,
  handleChange,
}) => {
  

  return (
    <div className="flex flex-col gap-10 text-start">
      <span>
        <label htmlFor="nombre_establecimiento">Nombre establecimiento</label>
        <Input
          onChange={handleChange}
          value={formData.nombre_establecimiento ?? ''}
          name={'nombre_establecimiento'}
        />
      </span>
      <div className="flex gap-5">
        
        {/* <span className="w-full">
          <label htmlFor="municipio">Municipio</label>
          <SelectMunicipios
            onChange={handleChange}
            department={departamentoSelect}
            value={formData.municipio}
            name={'municipio'}
          />
        </span> */}
      </div>
      <span>
        <label htmlFor="direccion_comercial">Dirección comercial:</label>
        <Input
          onChange={handleChange}
          value={formData.direccion_comercial}
          name={'direccion_comercial'}
        />
      </span>
      <span>
        <label htmlFor="telefono">Telefono:</label>
        <Input
          type="number"
          onChange={handleChange}
          value={formData.telefono}
          name={'telefono'}
        />
      </span>
      <span>
        <label htmlFor="email">Correo:</label>
        <Input
          type="email"
          onChange={handleChange}
          value={formData.email}
          name={'email'}
        />
      </span>
    </div>
  );
};
