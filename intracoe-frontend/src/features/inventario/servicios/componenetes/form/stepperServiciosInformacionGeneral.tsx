import React, { useEffect, useRef, useState } from 'react';
import { Input } from '../../../../../shared/forms/input';
import { ProductoRequest } from '../../../../../shared/interfaces/interfaces';
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
import { getAllTipoItem } from '../../../../../shared/services/productos/productosServices';

interface StepperInformacionGeneralProps {
  formData: ProductoRequest;
  handleChange: any;
}

export const StepperInformacionGeneral: React.FC<
  StepperInformacionGeneralProps
> = ({ formData, handleChange }) => {
  const [tipoItem, setTipoItem] = useState();

  const toast = useRef<Toast>(null);
  const [totalSize, setTotalSize] = useState(0);
  const fileUploadRef = useRef<FileUpload>(null);

  const onImageSelect = (e: FileUploadSelectEvent) => {
    const file = e.files[0] as File;
    handleChange({ target: { name: 'imagen', value: file } });
  };

  useEffect(() => {
    fetchTipoItem();
  }, []);

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

    setTotalSize(_totalSize);
    toast.current?.show({
      severity: 'info',
      summary: 'Success',
      detail: 'File Uploaded',
    });
  };

  const onTemplateRemove = (file: File, callback: Function) => {
    setTotalSize(totalSize - file.size);
    callback();
  };

  const onTemplateClear = () => {
    setTotalSize(0);
  };

  const headerTemplate = (options: FileUploadHeaderTemplateOptions) => {
    const { className, chooseButton, uploadButton, cancelButton } = options;
    const value = totalSize / 10000;
    const formatedValue =
      fileUploadRef && fileUploadRef.current
        ? fileUploadRef.current.formatSize(totalSize)
        : '0 B';

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
        {uploadButton}
        {cancelButton}
        <div className="align-items-center ml-auto flex gap-3">
          <span>{formatedValue} / 1 MB</span>
          <ProgressBar
            value={value}
            showValue={false}
            style={{ width: '10rem', height: '12px' }}
          ></ProgressBar>
        </div>
      </div>
    );
  };

  const itemTemplate = (inFile: object, props: ItemTemplateOptions) => {
    const file = inFile as File;
    return (
      <div className="align-items-center flex flex-wrap">
        <div className="align-items-center flex" style={{ width: '40%' }}>
          <img
            alt={file.name}
            role="presentation"
            src={URL.createObjectURL(file)}
            width={100}
          />

          <span className="flex-column ml-3 flex text-left">{file.name}</span>
        </div>
        <Button
          type="button"
          icon={<IoClose />}
          className="p-button-outlined p-button-rounded p-button-danger ml-auto"
          onClick={() => onTemplateRemove(file, props.onRemove)}
        />
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
      {/* <span>
        <label htmlFor="tipo_documento" className="flex">
          <span className="text-red pr-1">*</span> Imagen
        </label>
        <Toast ref={toast}></Toast>

        <Tooltip target=".custom-choose-btn" content="Escoger imagen" position="bottom" />
        <Tooltip target=".custom-upload-btn" content="Subir imagen" position="bottom" />
        <Tooltip target=".custom-cancel-btn" content="Limpiar" position="bottom" />
        <FileUpload
          ref={fileUploadRef}
          name="demo[]"
          customUpload      // para que no intente enviarla solo
          onSelect={onImageSelect}
          accept="image/*"
          maxFileSize={1000000}
          onUpload={onTemplateUpload}
          onError={onTemplateClear}
          onClear={onTemplateClear}
          headerTemplate={headerTemplate}
          itemTemplate={itemTemplate}
          emptyTemplate={emptyTemplate}
          chooseOptions={chooseOptions}
          uploadOptions={uploadOptions}
          cancelOptions={cancelOptions} />
      </span> */}
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
