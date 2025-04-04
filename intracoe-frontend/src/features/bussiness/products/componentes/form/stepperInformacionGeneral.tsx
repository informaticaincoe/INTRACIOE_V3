import React, { useEffect, useState } from 'react';
import { Input } from '../../../../../shared/forms/input';
import { ProductoRequest } from '../../../../../shared/interfaces/interfaces';
import { getAllTipoItem, getAllUnidadesDeMedida } from '../../services/productsServices';
import { Dropdown } from 'primereact/dropdown';
import { FileUpload, FileUploadHeaderTemplateOptions } from 'primereact/fileupload';

import { GrAdd } from "react-icons/gr";
import { LuUpload } from "react-icons/lu";
import { IoMdClose } from "react-icons/io";

interface StepperInformacionGeneralProps {
  formData: ProductoRequest;
  setFormData: any;
  handleChange: any;
}

export const StepperInformacionGeneral: React.FC<
  StepperInformacionGeneralProps
> = ({ formData, setFormData, handleChange }) => {
  const [unidadDeMedida, setUnidadDeMedida] = useState();
  const [tipoItem, setTipoItem] = useState();

  useEffect(() => {
    fetchUnidadesDeMedida();
    fetchTipoItem()
  }, []);

  const fetchUnidadesDeMedida = async () => {
    try {
      const response = await getAllUnidadesDeMedida();
      setUnidadDeMedida(response);
    } catch (error) {
      console.log(error);
    }
  };

  const fetchTipoItem = async () => {
    try {
      const response = await getAllTipoItem();
      setTipoItem(response);
    } catch (error) {
      console.log(error);
    }
  };

  const headerTemplate = (options: FileUploadHeaderTemplateOptions) => {
    const { className, chooseButton, uploadButton, cancelButton } = options;

    return (
      <div className={className} style={{ backgroundColor: 'transparent', display: 'flex', alignItems: 'center' }}>
        {chooseButton}
        {uploadButton}
        {cancelButton}
      </div>
    );
  };

  const chooseOptions = {
    icon:
      <span className='pr-2'>
        <GrAdd size={20} />
      </span>,
    iconOnly: false,
  };
  const uploadOptions = {
    icon:
      <span className='pr-2'>
        <LuUpload size={20} />
      </span>,
    iconOnly: false,
  };
  const cancelOptions = {
    icon:
      <span className='pr-2'>
        <IoMdClose size={22} />
      </span>,
    iconOnly: false,
  };

  return (
    <div className='flex flex-col gap-5'>
      <span>
        <label htmlFor="tipo_documento" className="flex">
          <span className="text-red pr-1">*</span> Imagen
        </label>
        <FileUpload
          chooseOptions={chooseOptions}
          uploadOptions={uploadOptions}
          cancelOptions={cancelOptions}
          headerTemplate={headerTemplate}
          name="demo[]"
          url={'/api/upload'}
          accept="image/*"
          maxFileSize={1000000}
          emptyTemplate={<p className="m-0">Arrastre y suelte archivos aquí para cargarlos.</p>}
          chooseLabel="Seleccionar"
          uploadLabel='Subir'
          cancelLabel='cancelar'
        />
      </span>
      <span>
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
          <span className="text-red pr-1">*</span> Unidad de medida
        </label>
        <Dropdown
          name="unidad_medida"
          value={formData.unidad_medida}
          onChange={(e) =>
            handleChange({ target: { name: 'unidad_medida', value: e.value } })
          }
          options={unidadDeMedida}
          optionLabel="descripcion"
          optionValue="id"
          placeholder="Seleccionar unidad de medida"
          className="md:w-14rem w-full text-start"
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
            name="descripcion"
            value={formData.descripcion}
            onChange={handleChange}
          />
        </span>
        <span className='w-full'>
          <label htmlFor="tipo_documento" className="flex">
            <span className="text-red pr-1">*</span> Precio compra
          </label>
          <Input
            type="number"
            name="descripcion"
            value={formData.descripcion}
            onChange={handleChange}
          />
        </span>
        <span className='w-full'>
          <label htmlFor="tipo_documento" className="flex">
            <span className="text-red pr-1">*</span> Precio venta
          </label>
          <Input
            type="number"
            name="descripcion"
            value={formData.descripcion}
            onChange={handleChange}
          />
        </span>
      </div>
    </div>
  );
};
