import React, { useEffect } from 'react';
import { RequestEmpresa } from '../../../../../shared/interfaces/interfaces';
import { Input } from '../../../../../shared/forms/input';
import { SelectTipoIdDocumento } from '../../../../../shared/Select/selectTipoIdDocumento';
import { SelectActividadesEconomicas } from '../../../../../shared/Select/selectActividadesEconomicas';
import { SelectAmbienteComponent } from '../../../../../shared/Select/selectAmbienteComponent';
import { SelectTipoEstablecimiento } from '../../../../../shared/Select/selectTipoEstablecimiento';
import { Password } from 'primereact/password';

interface StepperConfiguracionFacturacionProp {
  formData: RequestEmpresa;
  handleChange: any;
}

export const StepperConfiguracionFacturacion: React.FC<
  StepperConfiguracionFacturacionProp
> = ({ formData, handleChange }) => {
  useEffect(() => {
    console.log('ttttttttttttt', formData.tipo_documento);
  });
  return (
    <div className="flex flex-col gap-10 text-start">
      <span>
        <label htmlFor="tipo_documento">
          Tipo de documento de identificación:
        </label>
        <SelectTipoIdDocumento
          onChange={handleChange}
          value={formData.tipo_documento}
          name={'tipo_documento'}
        />
      </span>
      <span>
        <label htmlFor="nit">Número de documento de identificación:</label>
        <Input onChange={handleChange} value={formData.nit} name={'nit'} />
      </span>
      <span>
        <label htmlFor="nrc">NRC:</label>
        <Input onChange={handleChange} value={formData.nrc} name={'nrc'} />
      </span>
      <span>
        <label htmlFor="nombre_comercial">Nombre comercial:</label>
        <Input
          onChange={handleChange}
          value={formData.nombre_comercial}
          name={'nombre_comercial'}
        />
      </span>
      <span>
        <label htmlFor="nombre_razon_social">Nombre o razón social:</label>
        <Input
          onChange={handleChange}
          value={formData.nombre_razon_social}
          name={'nombre_razon_social'}
        />
      </span>
      <span>
        <label htmlFor="ambiente">Ambiente:</label>
        <SelectAmbienteComponent
          onChange={handleChange}
          value={formData.ambiente}
          name={'ambiente'}
        />
      </span>
      <span>
        <label htmlFor="codigo_punto_venta">Código punto de venta:</label>
        <Input
          onChange={handleChange}
          value={formData.codigo_punto_venta}
          name={'codigo_punto_venta'}
        />
      </span>
      <span>
        <label htmlFor="codigo_establecimiento">
          Código de establecimiento:
        </label>
        <Input
          onChange={handleChange}
          value={formData.codigo_establecimiento}
          name={'codigo_establecimiento'}
        />
      </span>
      <span>
        <label htmlFor="actividades_economicas"> Actividad economica </label>
        <SelectActividadesEconomicas
          onChange={handleChange}
          value={formData.actividades_economicas ?? ''}
          name={'actividades_economicas'}
        />
      </span>
      <span>
        <label htmlFor="tipoestablecimiento">Tipo establecimiento:</label>
        <SelectTipoEstablecimiento
          onChange={handleChange}
          value={formData.tipoestablecimiento}
          name={'tipoestablecimiento'}
        />
      </span>
      <span className='flex flex-col'>
        <label htmlFor="clave_privada">Clave privada:</label>
        <Password
          className="w-full"
          style={{ width: '100%' }}
          value={formData.clave_privada}
          panelStyle={{ display: 'none' }}
          onChange={(e: React.ChangeEvent<HTMLInputElement>) => {
            handleChange({
              target: {
                name: 'clave_privada',  // Aquí deberías usar 'name' en lugar de una clave directamente
                value: e.target.value,
              },
            });
          }}
          toggleMask
        />

      </span>
      <span>
        <label htmlFor="email">Clave publica:</label>
        <Password
          className="w-full"
          style={{ width: '100%' }}
          value={formData.clave_publica}
          panelStyle={{ display: 'none' }}
          onChange={(e: React.ChangeEvent<HTMLInputElement>) => {
            handleChange({
              target: {
                name: 'clave_publica',  // Aquí deberías usar 'name' en lugar de una clave directamente
                value: e.target.value,
              },
            });
          }}
          toggleMask
        />

      </span>
    </div>
  );
};
