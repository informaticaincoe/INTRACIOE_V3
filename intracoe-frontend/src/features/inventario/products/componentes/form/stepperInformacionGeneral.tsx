import React, { useEffect, useRef, useState } from 'react';
import { Input } from '../../../../../shared/forms/input';
import { ProductoRequest } from '../../../../../shared/interfaces/interfaces';
import { Dropdown } from 'primereact/dropdown';
import {
  FileUpload,
  FileUploadHeaderTemplateOptions,
  FileUploadSelectEvent,
  FileUploadUploadEvent,
} from 'primereact/fileupload';

import { GrAdd } from 'react-icons/gr';
import { LuUpload } from 'react-icons/lu';
import { IoMdClose } from 'react-icons/io';
import { Tooltip } from 'primereact/tooltip';
import { Toast } from 'primereact/toast';
import {
  getAllTipoItem,
  getAllUnidadesDeMedida,
} from '../../../../../shared/services/productos/productosServices';

interface StepperInformacionGeneralProps {
  formData: ProductoRequest;
  handleChange: any;
}

export const StepperInformacionGeneral: React.FC<
  StepperInformacionGeneralProps
> = ({ formData, handleChange }) => {
  const [unidadDeMedida, setUnidadDeMedida] = useState();
  const [tipoItem, setTipoItem] = useState();

  const toast = useRef<Toast>(null);
  const fileUploadRef = useRef<FileUpload>(null);

  const onImageSelect = (e: FileUploadSelectEvent) => {
    const file = e.files[0] as File;
    handleChange({ target: { name: 'imagen', value: file } });
  };

  useEffect(() => {
    fetchUnidadesDeMedida();
    fetchTipoItem();
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

  const onTemplateUpload = (e: FileUploadUploadEvent) => {
    let _totalSize = 0;

    e.files.forEach((file) => {
      _totalSize += file.size || 0;
    });

    toast.current?.show({
      severity: 'info',
      summary: 'Success',
      detail: 'File Uploaded',
    });
  };

  const headerTemplate = (options: FileUploadHeaderTemplateOptions) => {
    const { className, chooseButton, cancelButton } = options;

    return (
      <div
        className={className}
        style={{
          backgroundColor: 'transparent',
          display: 'flex',
          alignItems: 'center',
        }}
      >
        {chooseButton}
        {cancelButton}
        
      </div>
    );
  };

  const itemTemplate = (inFile: object) => {
    const file = inFile as File;
    return (
      <div className="align-items-center flex flex-wrap w-full justify-between">
        <div className="align-items-center flex" style={{ width: '40%' }}>
          <img
            alt={file.name}
            role="presentation"
            src={URL.createObjectURL(file)}
            width={100}
          />

          <span className="ml-3 flex text-left wrap-break-word">{file.name}</span>
        </div>
      </div>
    );
  };

  const emptyTemplate = () => {
    return (
      <div className="align-items-center flex-column flex">
        <i
          className="pi pi-image mt-3 p-5"
          style={{
            fontSize: '5em',
            borderRadius: '50%',
            backgroundColor: 'var(--surface-b)',
            color: 'var(--surface-d)',
          }}
        ></i>
        <span
          style={{ fontSize: '1.2em', color: 'var(--text-color-secondary)' }}
          className="my-5"
        >
          Drag and Drop Image Here
        </span>
      </div>
    );
  };

  const chooseOptions = {
    icon: (
      <span>
        <GrAdd size={20} />
      </span>
    ),
    iconOnly: true,
    className: 'custom-choose-btn p-button-rounded p-button-outlined',
  };
  const uploadOptions = {
    icon: (
      <span>
        <LuUpload size={20} />
      </span>
    ),
    iconOnly: true,
    className:
      'custom-upload-btn p-button-rounded p-button-success p-button-outlined',
  };
  const cancelOptions = {
    icon: (
      <span>
        <IoMdClose size={22} />
      </span>
    ),
    iconOnly: true,
    className:
      'custom-cancel-btn p-button-rounded p-button-danger p-button-outlined',
  };

  return (
    <div className="flex flex-col gap-8">
      <span>
        <label htmlFor="tipo_documento" className="flex">
          <span className="text-red pr-1">*</span> Codigo
        </label>
        <Input name="codigo" value={formData.codigo} onChange={handleChange} />
      </span>
      <span>
        <label htmlFor="tipo_documento" className="flex">
          <span className="text-red pr-1">*</span> Imagen
        </label>
        <Toast ref={toast}></Toast>

        <Tooltip
          target=".custom-choose-btn"
          content="Escoger imagen"
          position="bottom"
        />
        <Tooltip
          target=".custom-cancel-btn"
          content="Limpiar"
          position="bottom"
        />
        <FileUpload
          ref={fileUploadRef}
          name="demo[]"
          customUpload // para que no intente enviarla solo
          onSelect={onImageSelect}
          accept="image/*"
          maxFileSize={1000000}
          onUpload={onTemplateUpload}
          headerTemplate={headerTemplate}
          itemTemplate={itemTemplate}
          emptyTemplate={emptyTemplate}
          chooseOptions={chooseOptions}
          uploadOptions={uploadOptions}
          cancelOptions={cancelOptions}
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
      <div className="flex w-full gap-5">
        <span className="w-full">
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
        <span className="w-full">
          <label htmlFor="tipo_documento" className="flex">
            <span className="text-red pr-1">*</span> Precio compra
          </label>
          <Input
            type="number"
            name="precio_compra"
            value={formData.precio_compra.toString()}
            onChange={handleChange}
          />
        </span>
        <span className="w-full">
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
      </div>
    </div>
  );
};
