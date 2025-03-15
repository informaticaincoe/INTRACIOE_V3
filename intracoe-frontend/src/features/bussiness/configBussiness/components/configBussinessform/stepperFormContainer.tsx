import { Stepper } from 'primereact/stepper';
import { StepperPanel } from 'primereact/stepperpanel';
import { Button } from 'primereact/button';
import { useRef, useState } from 'react';
import { WhiteSectionsPage } from '../../../../../shared/containers/whiteSectionsPage';
import { StepperConfigBill } from './stepperConfigBill';
import StepperContactinfo from './stepperContactinfo';
import { createEmpresaById } from '../../services/empresaServices';
import { Empresa } from '../../interfaces/empresaInterfaces';

export const StepperContainer = () => {
  const stepperRef = useRef<Stepper | null>(null);

  const [formData, setFormData] = useState<Empresa>({
    tipo_documento:'',
    nit: '',
    nrc: '',
    nombre_establecimiento:'',
    nombre_comercial: '',
    nombre_razon_social: '',
    ambiente: '',
    codigo_punto_venta: '',
    codigo_establecimiento: '',
    actividades_economicas: [],
    tipoestablecimiento: '',
    municipio: '',
    direccion_comercial: '',
    telefono: '',
    email: '',
  });

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

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement>,
    formType: string
  ) => {
    if (formType === 'formData') {
      setFormData({ ...formData, [e.target.name]: e.target.value });
    }
  };

  const handleSendForm = async(e: React.FormEvent) => {
    e.preventDefault();
    console.log(formData);

    try {
      const response = await createEmpresaById(formData)
    } catch (error) {
      console.log(error)
    }

  };

  const handleSelectAmbiente = (value: string) => {
    setFormData({ ...formData, ambiente: value });
  };

  const handleSelectActividadesEconomicas = (value: string) => {
    console.log(value)
    // setFormData({ ...formData, actividadesEconomicas: value });
  };

  const handleTipoEstablecimiento = (value: string) => {
    console.log(value)

    // setFormData({ ...formData, tipoEstablecimiento: value });
  };

  const handleDepartamento = (value: string) => {
    console.log(value)

    // setFormData({ ...formData, departamento: value });
  };

  const handleMunicipio = (value: string) => {
    setFormData({ ...formData, municipio: value });
  };

  return (
    <WhiteSectionsPage className="mx-[20%]">
      <Stepper ref={stepperRef} style={{ flexBasis: '50rem' }}>
        <StepperPanel header="Configurar factura">
          <StepperConfigBill
            formData={formData}
            handleChange={(e: React.ChangeEvent<HTMLInputElement>) =>
              handleChange(e, 'formData')
            }
            handleSelectAmbiente={handleSelectAmbiente} // Pasar el manejador de select como prop
            handleSelectActividadesEconomicas={
              handleSelectActividadesEconomicas
            }
            handleTipoEstablecimiento={handleTipoEstablecimiento}
          />
          <div className="justify-content-end flex pt-4">
            <Button
              label="Siguiente"
              icon="pi pi-arrow-right"
              iconPos="right"
              onClick={handleNext}
            />
          </div>
        </StepperPanel>
        <StepperPanel header="Información de contacto">
          <StepperContactinfo
            formData={formData}
            handleChange={(e: React.ChangeEvent<HTMLInputElement>) =>
              handleChange(e, 'formData')
            }
            handleDepartamento={handleDepartamento}
            handleMunicipio={handleMunicipio}
          />
          <div className="flex w-full justify-between pt-4">
            <Button
              label="Atras"
              severity="secondary"
              icon="pi pi-arrow-left"
              onClick={handlePrev}
            />
            <Button
              label="Guardar"
              icon="pi pi-arrow-right"
              iconPos="right"
              onClick={handleSendForm}
            />
          </div>
        </StepperPanel>
      </Stepper>
    </WhiteSectionsPage>
  );
};
