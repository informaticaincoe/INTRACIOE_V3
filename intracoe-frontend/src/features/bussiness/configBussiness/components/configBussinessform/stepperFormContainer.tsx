import { Stepper } from 'primereact/stepper';
import { StepperPanel } from 'primereact/stepperpanel';
import { Button } from 'primereact/button';
import { useEffect, useRef, useState } from 'react';
import { WhiteSectionsPage } from '../../../../../shared/containers/whiteSectionsPage';
import { StepperConfigBill } from './stepperConfigBill';
import StepperContactinfo from './stepperContactinfo';
import {
  createEmpresaById,
  getAllEmpresas,
} from '../../services/empresaServices';
import {
  Ambiente,
  Departamento,
  EmisorInterface,
  Municipio,
  TipoDocumento,
  TipoEstablecimiento,
} from '../../interfaces/empresaInterfaces';
import { ActivitiesData } from '../../../../facturacion/activities/interfaces/activitiesData';
import { Toast } from 'primereact/toast';

export const StepperContainer = () => {
  const toast = useRef<Toast>(null);
  const stepperRef = useRef<Stepper | null>(null);

  const [formData, setFormData] = useState<EmisorInterface>({
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
  });

  const [error, setError] = useState({
    tipo_documento: '',
    nit: '',
    nrc: '',
    nombre_razon_social: '',
    actividades_economicas: '',
    ambiente: '',
    direccion_comercial: '',
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

  const handleSendForm = async (e: React.FormEvent) => {
    e.preventDefault();
    console.log('formData', formData);
    console.log('formDataAct', formData.actividades_economicas);

    let newErrors = {
      tipo_documento: '',
      nit: '',
      nrc: '',
      nombre_razon_social: '',
      actividades_economicas: '',
      direccion_comercial: '',
      ambiente: '',
    };

    if (formData.direccion_comercial === '') {
      newErrors.direccion_comercial = 'Campo obligatorio';
    }

    if (formData.nit === '') {
      newErrors.nit = 'Campo obligatorio';
    }

    if (formData.tipo_documento == null) {
      newErrors.tipo_documento = 'Campo obligatorio';
    }

    if (formData.nrc === '') {
      newErrors.nrc = 'Campo obligatorio';
    }

    if (formData.nombre_razon_social === '') {
      newErrors.nombre_razon_social = 'Campo obligatorio';
    }

    if (formData.ambiente.descripcion == '') {
      newErrors.ambiente = 'Campo obligatorio';
    }

    if (formData.actividades_economicas.length == 0) {
      newErrors.actividades_economicas = 'Campo obligatorio';
    }

    setError(newErrors);

    if (
      !newErrors.direccion_comercial &&
      !newErrors.nit &&
      !newErrors.tipo_documento &&
      !newErrors.nrc &&
      !newErrors.nombre_razon_social &&
      !newErrors.ambiente &&
      !newErrors.actividades_economicas
    ) {
      const body = {
        tipo_documento: formData.tipo_documento.id,
        nit: formData.nit,
        nrc: formData.nit,
        nombre_establecimiento: formData.nombre_establecimiento,
        nombre_comercial: formData.nombre_comercial,
        nombre_razon_social: formData.nombre_razon_social,
        ambiente: formData.ambiente.id,
        codigo_punto_venta: formData.codigo_punto_venta,
        codigo_establecimiento: formData.codigo_establecimiento,
        actividades_economicas: formData.actividades_economicas.map(
          (actividad) => actividad.id
        ), // Solo enviamos los IDs
        tipoestablecimiento: formData.tipoestablecimiento.id,
        departamento: formData.departamento.id,
        municipio: formData.municipio.id,
        direccion_comercial: formData.direccion_comercial,
        telefono: formData.telefono,
        email: formData.email,
      };

      console.log(body);

      try {
        const response = await createEmpresaById(body);
        showSuccess();
      } catch (error) {
        showError('Ya existe un emisor con este NIT');
        console.log('false');
      }
    } else {
      showError('Ingresar todos los campos obligatorios');
    }
  };

  const handleSelectAmbiente = (value: Ambiente) => {
    setFormData({ ...formData, ambiente: value });
  };

  const handleSelectActividadesEconomicas = (value: ActivitiesData[]) => {
    console.log(value);
    setFormData({ ...formData, actividades_economicas: value });
  };

  const handleTipoEstablecimiento = (value: TipoEstablecimiento) => {
    console.log(value);
    setFormData({ ...formData, tipoestablecimiento: value });
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

  const showSuccess = () => {
    if (toast.current) {
      toast.current.show({
        severity: 'success',
        summary: 'Guardado',
        detail: 'Configuración guardada con exito',
        life: 3000,
      });
    }
  };

  const showError = (message: string) => {
    if (toast.current) {
      toast.current.show({
        severity: 'error',
        summary: 'Error',
        detail: message,
        life: 3000,
      });
    }
  };

  useEffect(()=>{
    fetchInformacionEmpresa()
  },[])

  const fetchInformacionEmpresa = async() => {
    try {
      const response = await getAllEmpresas()
      console.log("response", response)
    } catch (error) {
      console.log(error)
    } 
  }

  return (
    <WhiteSectionsPage className="mx-[20%]">
      <>
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
              handleTipoDocId={handleTipoDocId}
              errores={error}
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
              errores={error}
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
        <Toast ref={toast} />
      </>
    </WhiteSectionsPage>
  );
};
