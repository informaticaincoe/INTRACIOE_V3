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
        <label htmlFor="nombreComercial">Nombre comercial</label>
        <Input
          name="nombreComercial"
          type="text"
          placeholder=""
          value={formData.nombreComercial}
          onChange={handleChange}
        />
      </span>
      <span className="w-full text-start">
        <label htmlFor="razonSocial">Nombre o razón social</label>
        <Input
          name="razonSocial"
          type="text"
          placeholder=""
          value={formData.razonSocial}
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
        <label htmlFor="codigoPuntoVenta">Código punto de venta</label>
        <Input
          name="codigoPuntoVenta"
          type="text"
          placeholder=""
          value={formData.codigoPuntoVenta}
          onChange={handleChange}
        />
      </span>
      <span className="w-full text-start">
        <label htmlFor="codigoEstablecimiento">Código de establecimiento</label>
        <Input
          name="codigoEstablecimiento"
          type="text"
          placeholder=""
          value={formData.codigoEstablecimiento}
          onChange={handleChange}
        />
      </span>
      <span className="w-full text-start">
        <label htmlFor="actividades-economicas">Actividades economicas</label>

        <SelectActividadesEconomicas
          actividades={formData.actividadesEconomicas}
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
