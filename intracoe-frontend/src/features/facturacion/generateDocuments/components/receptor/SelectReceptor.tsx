import { Dropdown } from 'primereact/dropdown';
import React, { useEffect, useState, useRef } from 'react';
import { Dialog } from 'primereact/dialog';
import { Stepper } from 'primereact/stepper';
import { StepperPanel } from 'primereact/stepperpanel';
import { Button } from 'primereact/button';
import { Input } from '../../../../../shared/forms/input';
import { SelectTipoIdDocumento } from '../../../../../shared/Select/selectTipoIdDocumento';
import { SelectActividadesEconomicas } from '../../../../../shared/Select/selectActividadesEconomicas';
import { ActivitiesData } from '../../../activities/interfaces/activitiesData';
import { RadioButton, RadioButtonChangeEvent } from 'primereact/radiobutton';
import {
  Ambiente,
  Departamento,
  Municipio,
  TipoDocumento,
  TipoEstablecimiento,
} from '../../../../bussiness/configBussiness/interfaces/empresaInterfaces';
import { SelectDepartmentComponent } from '../../../../../shared/Select/selectDepartmentComponent';
import { SelectMunicipios } from '../../../../../shared/Select/selectMunicipios';

const receptorData = [
  {
    id: 1,
    num_documento: '06142802961066',
    nombre: '06142802961066 - Francisco Antonio Flores',
  },
  {
    id: 2,
    num_documento: '062280967',
    nombre: '06142802961066 - Dominick Norberto Hernandez Alfaro',
  },
];

interface formData {
  nit: string;
  nrc: string;
  nombre_razon_social: string;
  nombre_comercial: string;
  direccion_comercial: string;
  telefono: string;
  email: string;
  codigo_establecimiento: string;
  codigo_punto_venta: string;
  nombre_establecimiento: string | null;
  tipoestablecimiento: TipoEstablecimiento;
  departamento: Departamento;
  municipio: Municipio;
  ambiente: Ambiente;
  tipo_documento: TipoDocumento;
  actividades_economicas: ActivitiesData[];
  direccion: string;
}

export const SelectReceptor = () => {
  const [selectedReceptor, setSelectedReceptor] = useState<any>('');
  const [receptorAuxData, setReceptorAuxData] = useState<any[]>([]);
  const [visibleModal, setVisibleModal] = useState(false);
  const [tipoIdDocumento, setTipoIdDocumento] = useState<{
    name?: string;
  } | null>(null);
  const [receptor, setTipoReceptor] = useState<string>('');

  const stepperRef = useRef<any>(null);

  useEffect(() => {
    fetchTipoDte();
  }, []);

  const fetchTipoDte = async () => {
    setReceptorAuxData(receptorData);
  };

  const [formData, setFormData] = useState<formData>({
    tipo_documento: { id: '', descripcion: '', code: '' },
    nit: '',
    nrc: '',
    nombre_establecimiento: '',
    nombre_comercial: '',
    nombre_razon_social: '',
    ambiente: { id: '', descripcion: '', code: '' },
    codigo_punto_venta: '',
    codigo_establecimiento: '',
    actividades_economicas: [],
    tipoestablecimiento: { id: '', descripcion: '', code: '' },
    departamento: { id: '', descripcion: '', code: '' },
    municipio: { id: '', descripcion: '', code: '' },
    direccion_comercial: '',
    telefono: '',
    email: '',
    direccion: '',
  });

  const handleSelectActividadesEconomicas = (value: ActivitiesData[]) => {
    console.log(value);
    setFormData({ ...formData, actividades_economicas: value });
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };
  const handleDepartamento = (value: Departamento) => {
    console.log(value);

    setFormData({ ...formData, departamento: value });
  };

  const handleMunicipio = (value: Municipio) => {
    setFormData({ ...formData, municipio: value });
  };

  const handleTipoDocId = (value: TipoDocumento) => {
    setFormData({ ...formData, tipo_documento: value });
  };

  const handleNext = () => {
    if (stepperRef.current) {
      stepperRef.current.nextCallback();
    }
  };

  const handlePrev = () => {
    if (stepperRef.current) {
      stepperRef.current.prevCallback();
    }
  };

  return (
    <>
      <div className="flex flex-col items-start gap-1">
        <label htmlFor={selectedReceptor.id} className="opacity-70">
          Receptor
        </label>
        <div className="flex w-full justify-between gap-10">
          <Dropdown
            id={selectedReceptor.id}
            value={selectedReceptor}
            onChange={(e: { value: any }) => setSelectedReceptor(e.value)}
            options={receptorAuxData}
            optionLabel="nombre"
            optionValue="num_documento"
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
                  <label htmlFor="">Nombre o razón social</label>
                  <Input
                    name="razon_social"
                    placeholder="Nombre o razón social"
                    type="text"
                    value={formData.nombre_razon_social}
                    onChange={handleChange}
                  />
                </span>
                <span>
                  <label htmlFor="">Nombre o razón social</label>
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
                    value={formData.nit}
                    onChange={handleChange}
                  />
                </span>
                <span>
                  <label htmlFor="">Actividad economica</label>
                  <SelectActividadesEconomicas
                    actividades={formData.actividades_economicas}
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
                          checked={receptor === 'natural'}
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
                          checked={receptor === 'juridica'}
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
                    onClick={() => stepperRef.current.nextCallback()}
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
                  <SelectDepartmentComponent
                    department={formData.departamento}
                    setDepartment={handleDepartamento}
                  />
                </span>
                <span>
                  <label htmlFor="">Municipio</label>
                  <SelectMunicipios
                    department={formData.departamento}
                    municipio={formData.municipio}
                    setMunicipio={handleMunicipio}
                  />
                </span>
                <span>
                  <label htmlFor="num_documento">Direccion</label>
                  <Input
                    name="direccion"
                    placeholder=""
                    type="text"
                    value={formData.direccion}
                    onChange={handleChange}
                  />
                </span>
                <span>
                  <label htmlFor="num_documento">Teléfono</label>
                  <Input
                    name="telefono"
                    placeholder=""
                    type="text"
                    value={formData.telefono}
                    onChange={handleChange}
                  />
                </span>
                <span>
                  <label htmlFor="num_documento">Correo</label>
                  <Input
                    name="email"
                    placeholder=""
                    type="text"
                    value={formData.email}
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
                    onClick={() => stepperRef.current.prevCallback()}
                  />
                  <Button
                    label="Guardar"
                    onClick={() => stepperRef.current.nextCallback()}
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
