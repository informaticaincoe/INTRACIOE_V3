import React, { useEffect, useState } from 'react';
import { Input } from '../../../../../shared/forms/input';
import { SelectAmbienteComponent } from '../../../../../shared/Select/selectAmbienteComponent';
import { SelectActividadesEconomicas } from '../../../../../shared/Select/selectActividadesEconomicas';
import { SelectTipoEstablecimiento } from '../../../../../shared/Select/selectTipoEstablecimiento';

export const StepperConfigBill = ({
  formData,
  handleChange,
  handleSelectAmbiente,
  handleSelectActividadesEconomicas,
  handleTipoEstablecimiento,
}: {
  formData: any;
  handleChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  handleSelectAmbiente: (value: string) => void;
  handleSelectActividadesEconomicas: (value: string) => void;
  handleTipoEstablecimiento: (value: string) => void;
}) => {
  return (
    <form className="flex flex-col gap-5">
      <span className="w-full text-start">
        <label htmlFor="tipo_documento" className="">
          Tipo de documento
        </label>
        <Input
          name="tipo_documento"
          type="text"
          placeholder=""
          value={formData.tipo_documento}
          onChange={handleChange}
        />
      </span>
      <span className="w-full text-start">
        <label htmlFor="nit" className="">
          NIT de emisor
        </label>
        <Input
          name="nit"
          type="text"
          placeholder=""
          value={formData.nit}
          onChange={handleChange}
        />
      </span>
      <span className="w-full text-start">
        <label htmlFor="nrc">NRC</label>
        <Input
          name="nrc"
          type="text"
          placeholder=""
          value={formData.nrc}
          onChange={handleChange}
        />
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
        <label htmlFor="nombre_razon_social">Nombre o razón social</label>
        <Input
          name="nombre_razon_social"
          type="text"
          placeholder=""
          value={formData.nombre_razon_social}
          onChange={handleChange}
        />
      </span>
      <span className="w-full text-start">
        <label htmlFor="ambiente">Ambientes</label>
        <SelectAmbienteComponent
          ambiente={formData.ambiente} // Pasamos el valor actual de 'ambiente'
          setSelectAmbiente={handleSelectAmbiente} // Pasamos la función que actualiza el estado
        />
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
        <label htmlFor="codigo_establecimiento">Código de establecimiento</label>
        <Input
          name="codigo_establecimiento"
          type="text"
          placeholder=""
          value={formData.codigo_establecimiento}
          onChange={handleChange}
        />
      </span>
      <span className="w-full text-start">
        <label htmlFor="actividades_economicas">Actividades economicas</label>

        <SelectActividadesEconomicas
          actividades={formData.actividades_economicas}
          setActividades={handleSelectActividadesEconomicas}
        />
      </span>
      <span className="w-full text-start">
        <label htmlFor="tipo-establecimiento">Tipo de establecimiento</label>
        <SelectTipoEstablecimiento
          tipoEstablecimiento={formData.tipoEstablecimiento}
          setTipoEstablecimiento={handleTipoEstablecimiento}
        />
      </span>
    </form>
  );
};
