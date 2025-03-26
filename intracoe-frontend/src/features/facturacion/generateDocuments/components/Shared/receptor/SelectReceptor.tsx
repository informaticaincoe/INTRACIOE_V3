import { Dropdown } from 'primereact/dropdown';
import React, { useEffect, useState, useRef } from 'react';
import { Dialog } from 'primereact/dialog';
import { Stepper } from 'primereact/stepper';
import { StepperPanel } from 'primereact/stepperpanel';
import { Button } from 'primereact/button';
import { Input } from '../../../../../../shared/forms/input';
import { SelectTipoIdDocumento } from '../../../../../../shared/Select/selectTipoIdDocumento';
import { SelectActividadesEconomicas } from '../../../../../../shared/Select/selectActividadesEconomicas';
import { RadioButton, RadioButtonChangeEvent } from 'primereact/radiobutton';
import { SelectDepartmentComponent } from '../../../../../../shared/Select/selectDepartmentComponent';
import { SelectMunicipios } from '../../../../../../shared/Select/selectMunicipios';
import { getAllReceptor } from '../../../services/receptor/receptorServices';
import { ActivitiesData, Departamento, Municipio, ReceptorInterface, TipoDocumento } from '../../../../../../shared/interfaces/interfaces';


interface StepperProps {
  receptor: ReceptorInterface,
  setReceptor:(receptor:ReceptorInterface) => void
}

export const SelectReceptor:React.FC<StepperProps> = ({receptor, setReceptor}) => {
  const [receptoresList, setReceptoreLists] = useState<ReceptorInterface[]>([]);
  const [visibleModal, setVisibleModal] = useState(false);
  const [tipoIdDocumento, setTipoIdDocumento] = useState<{
    name?: string;
  } | null>(null);
  const [tipoReceptor, setTipoReceptor] = useState<string>('');

  const stepperRef = useRef<Stepper | null>(null); // TODO: Tipar correctamente el ref

  useEffect(() => {
    fetchReceptores()
  }, []);


  const fetchReceptores = async () => {
    try {
      const response = await getAllReceptor()
      setReceptoreLists(response);
    }
    catch (error) {
      console.log(error)
    }
  };

  const handleSelectActividadesEconomicas = (value: ActivitiesData[]) => {
    console.log(value);
    setReceptor({ ...receptor, actividades_economicas: value });
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setReceptor({ ...receptor, [e.target.name]: e.target.value });
  };

  // const handleDepartamento = (value: Departamento) => {
  //   console.log(value);

  //   setReceptor({ ...receptor, departamento: value });
  // };

  const handleMunicipio = (value: Municipio) => {
    setReceptor({ ...receptor, municipio: value });
  };

  const handleTipoDocId = (value: TipoDocumento) => {
    setReceptor({ ...receptor, tipo_documento: value });
  };

  return (
    <>
      <div className="flex flex-col items-start gap-1">
        <label htmlFor={receptor.id} className="opacity-70">
          Receptor
        </label>
        <div className="flex w-full justify-between gap-10">
          <Dropdown
            id={receptor.id}
            value={receptor}
            onChange={(e: { value: any }) => setReceptor(e.value)}
            options={receptoresList}
            optionLabel="nombre"
            placeholder="Seleccione un receptor"
            className="font-display w-full text-start"
          />
          <button
            className="bg-primary-blue rounded-md px-5 py-2 text-nowrap text-white hover:cursor-pointer"
            onClick={() => setVisibleModal(true)}
          >
            Añadir nuevo receptor
          </button>
        </div>
      </div>
      <Dialog
        header={<p className="text-xl">Nuevo receptor</p>}
        visible={visibleModal}
        modal
        style={{ width: 'auto' }}
        onHide={() => {
          if (!visibleModal) return;
          setVisibleModal(false);
        }}
      >
        <div className="card justify-content-center flex">
          <Stepper ref={stepperRef} style={{ flexBasis: '50rem' }}>
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
                    value={receptor.num_documento}
                    onChange={handleChange}
                  />
                </span>
                <span>
                  <label htmlFor="">Actividad economica</label>
                  <SelectActividadesEconomicas
                    actividades={receptor.actividades_economicas}
                    setActividades={handleSelectActividadesEconomicas}
                    className={'selectActReceptor'}
                  />
                </span>
                <span className="flex flex-col gap-2">
                  <label htmlFor="">Tipo de receptor</label>
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
                    department={receptor.departamento}
                    setDepartment={handleDepartamento}
                  /> */}
                </span>
                <span>
                  <label htmlFor="">Municipio</label>
                  <SelectMunicipios
                    department={receptor.municipio}
                    municipio={receptor.municipio}
                    setMunicipio={handleMunicipio}
                  />
                </span>
                <span>
                  <label htmlFor="direccion">Direccion</label>
                  <Input
                    name="direccion"
                    placeholder=""
                    type="text"
                    value={receptor.direccion}
                    onChange={handleChange}
                  />
                </span>
                <span>
                  <label htmlFor="telefono">Teléfono</label>
                  <Input
                    name="telefono"
                    placeholder=""
                    type="text"
                    value={receptor.telefono}
                    onChange={handleChange}
                  />
                </span>
                <span>
                  <label htmlFor="num_documento">Correo</label>
                  <Input
                    name="email"
                    placeholder=""
                    type="text"
                    value={receptor.correo}
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
          </Stepper>
        </div>
      </Dialog>
    </>
  );
};