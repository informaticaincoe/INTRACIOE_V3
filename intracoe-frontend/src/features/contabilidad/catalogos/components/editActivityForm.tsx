import { Dispatch, SetStateAction, useEffect, useState } from 'react';
import { Dialog } from 'primereact/dialog';
import React from 'react';
import { Input } from '../../../../shared/forms/input';
import { getAllDepartamentos } from '../../../bussiness/configBussiness/services/ubicacionService';
import { Dropdown } from 'primereact/dropdown';
import { SelectPaisComponent } from '../../../../shared/Select/selectPais';

interface EditActivityProps {
  catalogo: string;
  item: any;
  visible: boolean;
  setVisible: Dispatch<SetStateAction<boolean>>;
  onSave: () => Promise<void>;
  saveFunction: (id: number, data: any) => Promise<void>;
}

export const EditActivityForm: React.FC<EditActivityProps> = ({
  catalogo,
  item,
  visible,
  setVisible,
  onSave,
  saveFunction,
}) => {
  const [departamentoSelect, setDepartamentoSelect] = useState();
  const [formData, setFormData] = useState(item);
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };
  const [departmentList, setDepartmentList] = useState<any[]>([]);

  useEffect(() => {
    const fetchDepartaments = async () => {
      try {
        const response = await getAllDepartamentos();
        setDepartmentList(response);
      } catch (error) {
        console.log(error);
      }
    };

    fetchDepartaments();
  }, []);

  useEffect(() => {
    setFormData(item);

    if (item?.departamento && departmentList.length > 0) {
      setDepartamentoSelect(item.departamento?.id || item.departamento);
    }
  }, [item, departmentList]);

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

      case 'Departamentos':
        body = {
          codigo: formData.codigo,
          descripcion: formData.descripcion,
          pais: formData.pais?.id | formData.pais,
        };
        break;

      case 'municipios':
        body = {
          codigo: formData.codigo,
          descripcion: formData.descripcion,
          departamento: formData.departamento, // ya lo dejaste en forma de ID
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

    try {
      await saveFunction(formData.id, body);
      setVisible(false);
      onSave();
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

          {catalogo == 'Departamentos' && (
            <span className="flex flex-col pt-5">
              <label htmlFor="version" className="">
                Pais:
              </label>
              <SelectPaisComponent value={formData.pais?.id || formData.pais} onChange={handleChange} name={'pais'} />
            </span>
          )}

          {catalogo == 'municipios' && (
            <span className="flex flex-col pt-5">
              <label htmlFor="version" className="">
                Departamento:
              </label>
              <Dropdown
                value={departamentoSelect}
                onChange={(e) => {
                  setDepartamentoSelect(e.value);
                  setFormData((prev: any) => ({
                    ...prev,
                    departamento: e.value, // Esto guarda el ID también en formData
                  }));
                }}
                options={departmentList}
                optionLabel="descripcion"
                optionValue="id"
                placeholder="Seleccionar departamento"
                className="md:w-14rem font-display w-full"
                filter
              />

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
