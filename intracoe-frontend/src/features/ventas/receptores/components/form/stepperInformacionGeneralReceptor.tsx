import React from 'react';
import { ReceptorRequestInterface } from '../../../../../shared/interfaces/interfaces';
import { SelectTipoIdDocumento } from '../../../../../shared/Select/selectTipoIdDocumento';
import { Input } from '../../../../../shared/forms/input';
import { SelectActividadesEconomicas } from '../../../../../shared/Select/selectActividadesEconomicas';
import { RadioButton } from 'primereact/radiobutton';

interface StepperInformacionGeneralProps {
  formData: ReceptorRequestInterface;
  handleChange: any;
}

export const StepperInformacionGeneralReceptor: React.FC<
  StepperInformacionGeneralProps
> = ({ formData, handleChange }) => {
  return (
    <div className="flex flex-col gap-10 text-start">
      <span>
        <label htmlFor="nombre">Nombre</label>
        <Input
          onChange={handleChange}
          value={formData.nombre}
          name={'nombre'}
        />
      </span>
      <span>
        <label htmlFor="tipo_documento">
          {' '}
          Tipo de documento de identificación
        </label>
        <SelectTipoIdDocumento
          onChange={handleChange}
          value={formData.tipo_documento}
          name={'tipo_documento'}
        />
      </span>
      <span>
        <label htmlFor="num_documento">
          {' '}
          Numero de documento de identificación{' '}
        </label>
        <Input
          onChange={handleChange}
          value={formData.num_documento}
          name={'num_documento'}
        />
      </span>
      <span>
        <label htmlFor="tipó_documento_id"> Actividad economica </label>
        <SelectActividadesEconomicas
          onChange={handleChange}
          value={formData.actividades_economicas}
          name={'actividades_economicas'}
        />
      </span>
      <span>
        <label htmlFor="tipó_documento_id">Tipo de receptor</label>
        <div className="flex flex-wrap gap-3">
          <div className="align-items-center flex">
            <RadioButton
              inputId="tipoReceptor1"
              name="tipo_receptor"
              value="Natural"
              onChange={handleChange}
              checked={formData.tipo_receptor === 'Natural'}
            />
            <label htmlFor="tipoReceptor1" className="ml-2">
              Natural
            </label>
          </div>
          <div className="align-items-center flex">
            <RadioButton
              inputId="tipoReceptor2"
              name="tipo_receptor"
              value="Juridica"
              onChange={handleChange}
              checked={formData.tipo_receptor === 'Juridica'}
            />
            <label htmlFor="tipoReceptor2" className="ml-2">
              Juridica
            </label>
          </div>
        </div>
      </span>
    </div>
  );
};
