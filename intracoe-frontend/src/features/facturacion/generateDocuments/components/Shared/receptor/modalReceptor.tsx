import { Stepper } from 'primereact/stepper';
import React, { useRef, useState } from 'react';
import {
  ActivitiesData,
  Municipio,
  TipoDocumento,
} from '../../../../../../shared/interfaces/interfaces';
import { SelectTipoIdDocumento } from '../../../../../../shared/Select/selectTipoIdDocumento';
import { StepperPanel } from 'primereact/stepperpanel';
import { Input } from '../../../../../../shared/forms/input';
import { SelectActividadesEconomicas } from '../../../../../../shared/Select/selectActividadesEconomicas';
import { RadioButton, RadioButtonChangeEvent } from 'primereact/radiobutton';
import { Button } from 'primereact/button';
import { SelectMunicipios } from '../../../../../../shared/Select/selectMunicipios';

interface ModalReceptorinterfaceProp {
  setReceptoreLists: any;
  receptoresList: any;
}

export const ModalReceptor: React.FC<ModalReceptorinterfaceProp> = ({
  setReceptoreLists,
  receptoresList,
}) => {
  const [tipoIdDocumento, setTipoIdDocumento] = useState<{
    name?: string;
  } | null>(null);
  const [tipoReceptor, setTipoReceptor] = useState<string>('');
  const [visibleModal, setVisibleModal] = useState(false);

  const stepperRef = useRef<Stepper | null>(null); // TODO: Tipar correctamente el ref

  const handleSelectActividadesEconomicas = (value: ActivitiesData[]) => {
    setReceptoreLists({ ...receptoresList, actividades_economicas: value });
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setReceptoreLists({ ...receptoresList, [e.target.name]: e.target.value });
  };

  // const handleDepartamento = (value: Departamento) => {
  //   console.log(value);

  //   setReceptoreLists({ ...receptoresList, departamento: value });
  // };

  const handleMunicipio = (value: Municipio) => {
    setReceptoreLists({ ...receptoresList, municipio: value });
  };

  const handleTipoDocId = (value: TipoDocumento) => {
    setReceptoreLists({ ...receptoresList, tipo_documento: value });
  };

  return (
    <div className="card justify-content-center flex">
      <StepperPanel header="información general">
        <div className="flex flex-col gap-8">
          <span>
            <label htmlFor="">Tipo de documento de identificacion</label>
            <SelectTipoIdDocumento
              tipoIdDocumento={tipoIdDocumento}
              setTipoIdDocumento={setTipoIdDocumento}
            />
          </span>
          <span>
            <label htmlFor="num_documento">
              Número de documento de identificación (
              {tipoIdDocumento && tipoIdDocumento.name})
            </label>
            <Input
              name="num_documento"
              placeholder=""
              type="text"
              value={receptoresList.num_documento}
              onChange={handleChange}
            />
          </span>
          <span>
            <label htmlFor="">Actividad economica</label>
            <SelectActividadesEconomicas
              actividades={receptoresList.actividades_economicas}
              setActividades={handleSelectActividadesEconomicas}
              className={'selectActReceptor'}
            />
          </span>
          <span className="flex flex-col gap-2">
            <label htmlFor="">Tipo de receptoresList</label>
            <div className="justify-content-center flex">
              <div className="flex flex-wrap gap-5">
                <div className="align-items-center flex">
                  <RadioButton
                    inputId="natural"
                    name="natural"
                    value="natural"
                    onChange={(e: RadioButtonChangeEvent) =>
                      setTipoReceptor(e.value)
                    }
                    checked={tipoReceptor === 'natural'}
                  />
                  <label htmlFor="natural" className="ml-2">
                    Natural
                  </label>
                </div>
                <div className="align-items-center flex">
                  <RadioButton
                    inputId="juridica"
                    name="juridica"
                    value="juridica"
                    onChange={(e: RadioButtonChangeEvent) =>
                      setTipoReceptor(e.value)
                    }
                    checked={tipoReceptor === 'juridica'}
                  />
                  <label htmlFor="juridica" className="ml-2">
                    Juridica
                  </label>
                </div>
              </div>
            </div>
          </span>
        </div>
        <div className="w-full items-end justify-end">
          <div className="flex w-full items-end pt-4">
            <Button
              label="Siguiente"
              onClick={() => stepperRef.current?.nextCallback()}
              unstyled
              className="hover: bg-primary-blue mt-5 cursor-pointer self-end rounded-md px-6 py-3 text-white"
            />
          </div>
        </div>
      </StepperPanel>
      <StepperPanel header="Informacion de contacto">
        <div className="flex flex-col gap-8">
          <span>
            <label htmlFor="">Departamento</label>
            {/* <SelectDepartmentComponent
                    department={receptoresList.departamento}
                    setDepartment={handleDepartamento}
                  /> */}
          </span>
          <span>
            <label htmlFor="">Municipio</label>
            <SelectMunicipios
              department={receptoresList.municipio}
              municipio={receptoresList.municipio}
              setMunicipio={handleMunicipio}
            />
          </span>
          <span>
            <label htmlFor="direccion">Direccion</label>
            <Input
              name="direccion"
              placeholder=""
              type="text"
              value={receptoresList.direccion}
              onChange={handleChange}
            />
          </span>
          <span>
            <label htmlFor="telefono">Teléfono</label>
            <Input
              name="telefono"
              placeholder=""
              type="text"
              value={receptoresList.telefono}
              onChange={handleChange}
            />
          </span>
          <span>
            <label htmlFor="num_documento">Correo</label>
            <Input
              name="email"
              placeholder=""
              type="text"
              value={receptoresList.correo}
              onChange={handleChange}
            />
          </span>
        </div>
        <div className="w-full items-end justify-end">
          <div className="flex w-full items-end gap-3 pt-4">
            <Button
              label="Regresar"
              unstyled
              className="border-primary-blue text-primary-blue mt-5 cursor-pointer rounded-md border bg-white px-6 py-3 hover:cursor-pointer"
              onClick={() => stepperRef.current?.nextCallback()}
            />
            <Button
              label="Guardar"
              onClick={() => stepperRef.current?.prevCallback()}
              unstyled
              className="bg-primary-blue mt-5 cursor-pointer self-end rounded-md px-6 py-3 text-white hover:cursor-pointer"
            />
          </div>
        </div>
      </StepperPanel>
    </div>
  );
};
