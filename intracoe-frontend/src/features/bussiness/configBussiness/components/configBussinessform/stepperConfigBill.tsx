import React from 'react';
import { Input } from '../../../../../shared/forms/input';
import { SelectAmbienteComponent } from '../../../../../shared/Select/selectAmbienteComponent';
import { SelectActividadesEconomicas } from '../../../../../shared/Select/selectActividadesEconomicas';
import { SelectTipoEstablecimiento } from '../../../../../shared/Select/selectTipoEstablecimiento';
import { SelectTipoIdDocumento } from '../../../../../shared/Select/selectTipoIdDocumento';
import {
  Ambiente,
  TipoDocumento,
  TipoEstablecimiento,
} from '../../interfaces/empresaInterfaces';

export const StepperConfigBill = ({
  formData,
  handleChange,
  handleSelectAmbiente,
  handleSelectActividadesEconomicas,
  handleTipoEstablecimiento,
  handleTipoDocId,
  errores,
}: {
  formData: any;
  handleChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  handleSelectAmbiente: (value: Ambiente) => void;
  handleSelectActividadesEconomicas: (value: any) => void;
  handleTipoEstablecimiento: (value: TipoEstablecimiento) => void;
  handleTipoDocId: (value: TipoDocumento) => void;
  errores: any;
}) => {
  return (
    <form className="flex flex-col gap-5">
      <span className="w-full text-start">
        <label htmlFor="tipo_documento" className="">
          <span className="text-red pr-1">*</span> Tipo de documento
        </label>
        <SelectTipoIdDocumento
          tipoIdDocumento={formData.tipo_documento}
          setTipoIdDocumento={handleTipoDocId}
        />
        {errores.nit && (
          <span className="text-sm text-red-500">{errores.tipo_documento}</span>
        )}
      </span>
      <span className="w-full text-start">
        <label htmlFor="nit" className="">
          <span className="text-red pr-1">*</span>
          {formData.tipo_documento.name != 'Otro' ? (
            <span>{formData.tipo_documento.name} de emisor</span>
          ) : (
            <span>Número de documento</span>
          )}
        </label>
        <Input
          name="nit"
          type="text"
          placeholder=""
          value={formData.nit}
          onChange={handleChange}
        />
        {errores.nit && (
          <span className="text-sm text-red-500">{errores.nit}</span>
        )}
      </span>
      <span className="w-full text-start">
        <span className="text-red pr-1">*</span>

        <label htmlFor="nrc">NRC</label>
        <Input
          name="nrc"
          type="text"
          placeholder=""
          value={formData.nrc}
          onChange={handleChange}
        />
        {errores.nrc && (
          <span className="text-sm text-red-500">{errores.nrc}</span>
        )}
      </span>
      <span className="w-full text-start">
        <label htmlFor="nombre_comercial">Nombre comercial</label>
        <Input
          name="nombre_comercial"
          type="text"
          placeholder=""
          value={formData.nombre_comercial}
          onChange={handleChange}
        />
      </span>
      <span className="w-full text-start">
        <span className="text-red pr-1">*</span>
        <label htmlFor="nombre_razon_social">Nombre o razón social</label>
        <Input
          name="nombre_razon_social"
          type="text"
          placeholder=""
          value={formData.nombre_razon_social}
          onChange={handleChange}
        />
        {errores.nombre_razon_social && (
          <span className="text-sm text-red-500">
            {errores.nombre_razon_social}
          </span>
        )}
      </span>
      <span className="w-full text-start">
        <span className="text-red pr-1">*</span>
        <label htmlFor="ambiente">Ambiente</label>
        <SelectAmbienteComponent
          ambiente={formData.ambiente}
          setSelectAmbiente={handleSelectAmbiente}
        />
        {errores.ambiente && (
          <span className="text-sm text-red-500">{errores.ambiente}</span>
        )}
      </span>
      <span className="w-full text-start">
        <label htmlFor="codigo_punto_venta">Código punto de venta</label>
        <Input
          name="codigo_punto_venta"
          type="text"
          placeholder=""
          value={formData.codigo_punto_venta}
          onChange={handleChange}
        />
      </span>
      <span className="w-full text-start">
        <label htmlFor="codigo_establecimiento">
          Código de establecimiento
        </label>
        <Input
          name="codigo_establecimiento"
          type="text"
          placeholder=""
          value={formData.codigo_establecimiento}
          onChange={handleChange}
        />
      </span>
      <span className="w-full text-start">
        <label htmlFor="nombre_establecimiento">Nombre establecimiento</label>
        <Input
          name="nombre_establecimiento"
          type="text"
          placeholder=""
          value={formData.nombre_establecimiento}
          onChange={handleChange}
        />
      </span>
      <span className="w-full text-start">
        <span className="text-red pr-1">*</span>
        <label htmlFor="actividades_economicas">Actividades economicas</label>

        <SelectActividadesEconomicas
          actividades={formData.actividades_economicas}
          setActividades={handleSelectActividadesEconomicas}
        />
        {errores.actividades_economicas && (
          <span className="text-sm text-red-500">
            {errores.actividades_economicas}
          </span>
        )}
      </span>
      <span className="w-full text-start">
        <label htmlFor="tipo-establecimiento">Tipo de establecimiento</label>
        <SelectTipoEstablecimiento
          tipoEstablecimiento={formData.tipoestablecimiento}
          setTipoEstablecimiento={handleTipoEstablecimiento}
        />
      </span>
    </form>
  );
};
