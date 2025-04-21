import { useEffect, useState } from 'react';
import { Dialog } from 'primereact/dialog';
import React from 'react';
import { Input } from '../../../../shared/forms/input';
import { SelectDepartmentComponent } from '../../../../shared/Select/selectDepartmentComponent';
import { SelectPaisComponent } from '../../../../shared/Select/selectPais';

interface NewActivityProps {
  catalogo: string;
  visible: boolean;
  setVisible: any;
  createFunction: (data: any) => Promise<any>;
}

export const NewActivityForm: React.FC<NewActivityProps> = ({
  catalogo,
  visible,
  setVisible,
  createFunction,
}) => {
  const [departamentoSelect, setDepartamentoSelect] = useState();
  // const [paisSelect, setPaisSelect] = useState();
  const [formData, setFormData] = useState({
    codigo: '',
    descripcion: '',
    version: '', //Tipo de documento tributario electronico
    departamento: '',
    motivo_contingencia: '',
    pais: ''
  });
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  useEffect(() => {
    console.log(departamentoSelect);
  }, [departamentoSelect]);

  const handlerForm = async (e: React.FormEvent) => {
    e.preventDefault();

    let body: any = {};

    switch (catalogo) {
      case 'tipo documento tributario electronico':
        body = {
          codigo: formData.codigo,
          descripcion: formData.descripcion,
          version: formData.version,
          motivo_contingencia: formData.motivo_contingencia,
        };
        break;

      case 'municipios':
        body = {
          codigo: formData.codigo,
          descripcion: formData.descripcion,
          departamento: departamentoSelect,
        };
        break;

      case 'Departamentos':
        body = {
          codigo: formData.codigo,
          descripcion: formData.descripcion,
          pais: formData.pais,
        };
        break;

      case 'Tipo contingencia':
        body = {
          codigo: formData.codigo,
          descripcion: formData.descripcion,
          motivo_contingencia: formData.motivo_contingencia,
        };
        break;

      default:
        body = {
          codigo: formData.codigo,
          descripcion: formData.descripcion,
        };
        break;
    }

    console.log("bbbbbbbbbbbbbb",body)

    try {
      const response = await createFunction(body);
      setVisible(false);
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <>
      <Dialog
        header={<p className="px-5 text-xl font-bold">Nuevo {catalogo}</p>}
        visible={visible}
        style={{ width: '60vw' }}
        onHide={() => {
          if (!visible) return;
          setVisible(false);
        }}
      >
        <form className="flex flex-col gap-7 px-5">
          <span className="flex flex-col pt-5">
            <label htmlFor="code" className="">
              Codigo:
            </label>
            <Input
              name="codigo"
              placeholder="codigo"
              type="text"
              value={formData.codigo}
              onChange={handleChange}
            />
          </span>
          <span className="flex flex-col pt-5">
            <label htmlFor="code" className="">
              Descripción:
            </label>
            <Input
              name="descripcion"
              placeholder="descripcion"
              type="text"
              value={formData.descripcion}
              onChange={handleChange}
            />
          </span>
          {catalogo == 'tipo documento tributario electronico' && (
            <span className="flex flex-col pt-5">
              <label htmlFor="version" className="">
                Versión:
              </label>
              <Input
                name="version"
                placeholder="version"
                type="number"
                value={formData.version}
                onChange={handleChange}
              />
            </span>
          )}
          {catalogo == 'Tipo contingencia' && (
            <span className="flex flex-col pt-5">
              <label htmlFor="version" className="">
                Motivo contingencia:
              </label>
              <Input
                name="motivo_contingencia"
                placeholder="Motivo de contingencia"
                type="text"
                value={formData.motivo_contingencia}
                onChange={handleChange}
              />
            </span>
          )}
          {catalogo == 'municipios' && (
            <span className="flex flex-col pt-5">
              <label htmlFor="version" className="">
                Departamento:
              </label>
              <SelectDepartmentComponent
                setDepartamentoSelect={setDepartamentoSelect}
                departamentoSelect={departamentoSelect}
              />
            </span>
          )}

          {catalogo == 'Departamentos' && (
            <span className="flex flex-col pt-5">
              <label htmlFor="version" className="">
                Pais:
              </label>
              <SelectPaisComponent value={formData.pais} onChange={handleChange} name={'pais'} />
            </span>
          )}
          <span className="flex w-full justify-end gap-3">
            <button
              className="bg-primary-blue rounded-md px-6 py-3 text-white hover:cursor-pointer"
              onClick={handlerForm}
            >
              Guardar
            </button>
          </span>
        </form>
      </Dialog>
    </>
  );
};
