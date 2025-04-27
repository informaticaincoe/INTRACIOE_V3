import React, { useEffect, useRef, useState } from 'react';
import { Dropdown } from 'primereact/dropdown';
import {
  FileUpload,
  FileUploadHeaderTemplateOptions,
  FileUploadSelectEvent,
  FileUploadUploadEvent,
  ItemTemplateOptions,
} from 'primereact/fileupload';
import { GrAdd } from 'react-icons/gr';
import { LuUpload } from 'react-icons/lu';
import { IoMdClose } from 'react-icons/io';
import { Toast } from 'primereact/toast';
import { ProgressBar } from 'primereact/progressbar';
import { Button } from 'primereact/button';
import { IoClose } from 'react-icons/io5';
import { ReceptorRequestInterface } from '../../../../../../../shared/interfaces/interfaces';
import { Input } from '../../../../../../../shared/forms/input';
import { SelectTipoIdDocumento } from '../../../../../../../shared/Select/selectTipoIdDocumento';

interface StepperInformacionGeneralProps {
  formData: ReceptorRequestInterface;
  handleChange: any;
}

export const StepperInformacionGeneral: React.FC<
  StepperInformacionGeneralProps
> = ({ formData, handleChange }) => {
  const [tipoItem, setTipoItem] = useState();

  const toast = useRef<Toast>(null);

  return (
    <div className="flex flex-col gap-8">
      <span>
        <label htmlFor="tipo_documento" className="flex">
          <span className="text-red pr-1">*</span> Tipo de documento de
          identificacion
        </label>
        <SelectTipoIdDocumento
          name="tipo_documento_id"
          value={formData.tipo_documento_id}
          onChange={handleChange}
        />
      </span>

      {/* <span>
        <label htmlFor="tipo_documento" className="flex">
          <span className="text-red pr-1">*</span> Descripción
        </label>
        <Input
          name="descripcion"
          value={formData.descripcion}
          onChange={handleChange}
        />
      </span>
      <span>
        <label htmlFor="tipo_documento" className="flex">
          <span className="text-red pr-1">*</span> Tipo item
        </label>
        <Dropdown
          name="tipo_item"
          value={formData.tipo_item}
          onChange={(e) =>
            handleChange({ target: { name: 'tipo_item', value: e.value } })
          }
          options={tipoItem}
          optionLabel="descripcion"
          optionValue="id"
          placeholder="Seleccionar el tipo de item"
          className="md:w-14rem w-full text-start"
        />
      </span>
      <div className='flex w-full gap-5'>
        <span className='w-full'>
          <label htmlFor="tipo_documento" className="flex">
            <span className="text-red pr-1">*</span> Precio unitario
          </label>
          <Input
            type="number"
            name="preunitario"
            value={formData.preunitario.toString()}
            onChange={handleChange}
          />
        </span>
        <span className='w-full'>
          <label htmlFor="tipo_documento" className="flex">
            <span className="text-red pr-1">*</span> Precio venta
          </label>
          <Input
            type="number"
            name="precio_venta"
            value={formData.precio_venta.toString()}
            onChange={handleChange}
          />
        </span>
      </div> */}
    </div>
  );
};
