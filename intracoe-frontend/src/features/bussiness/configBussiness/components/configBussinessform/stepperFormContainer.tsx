import React, { useState, useEffect } from 'react';
import { Steps, message } from 'antd';
import {
  ActivitiesData,
  Ambiente,
  defaultEmisorData,
  Departamento,
  EmisorInterface,
  Municipio,
  TipoDocumento,
  TipoEstablecimiento,
} from '../../../../../shared/interfaces/interfaces';
import {
  createEmpresaById,
  getAllEmpresas,
} from '../../services/empresaServices';
import { StepperConfigBill } from './stepperConfigBill';
import StepperContactinfo from './stepperContactinfo';
import { WhiteSectionsPage } from '../../../../../shared/containers/whiteSectionsPage';

export const StepperContainer = () => {
  // Estado para controlar el paso actual
  const [current, setCurrent] = useState(0);

  // Estado del formulario y errores
  const [formData, setFormData] = useState<EmisorInterface>(defaultEmisorData);
  const [error, setError] = useState({
    tipo_documento: '',
    nit: '',
    nrc: '',
    nombre_razon_social: '',
    actividades_economicas: '',
    ambiente: '',
    direccion_comercial: '',
  });

  // Ejemplo de Toast con message de Ant Design
  const showSuccess = () => {
    message.success('Configuración guardada con éxito', 3);
  };

  const showError = (msg: string) => {
    message.error(msg, 3);
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
    // Validaciones...
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
    if (formData.ambiente.descripcion === '') {
      newErrors.ambiente = 'Campo obligatorio';
    }
    if (formData.actividades_economicas.length === 0) {
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
        ),
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
        console.log(response);
        showSuccess();
      } catch (error) {
        showError('Ya existe un emisor con este NIT');
        console.log('false');
      }
    } else {
      showError('Ingresar todos los campos obligatorios');
    }
  };

  // Métodos para actualizar formData desde los componentes hijos
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

  useEffect(() => {
    const fetchInformacionEmpresa = async () => {
      try {
        const response = await getAllEmpresas();
        console.log('response', response);
      } catch (error) {
        console.log(error);
      }
    };
    fetchInformacionEmpresa();
  }, []);

  // Definimos los pasos para el Stepper de Ant Design
  const steps = [
    {
      title: 'Configurar factura',
      content: (
        <>
          <StepperConfigBill
            formData={formData}
            handleChange={(e: React.ChangeEvent<HTMLInputElement>) =>
              handleChange(e, 'formData')
            }
            handleSelectAmbiente={handleSelectAmbiente}
            handleSelectActividadesEconomicas={
              handleSelectActividadesEconomicas
            }
            handleTipoEstablecimiento={handleTipoEstablecimiento}
            handleTipoDocId={handleTipoDocId}
            errores={error}
          />
          <div className="justify-content-end flex pt-4">
            <button onClick={() => setCurrent(current + 1)}>Siguiente</button>
          </div>
        </>
      ),
    },
    {
      title: 'Información de contacto',
      content: (
        <>
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
            <button onClick={() => setCurrent(current - 1)}>Atras</button>
            <button onClick={handleSendForm}>Guardar</button>
          </div>
        </>
      ),
    },
  ];

  return (
    <WhiteSectionsPage className="mx-[20%]">
      <>
        <Steps
          current={current}
          items={steps.map((item) => ({ key: item.title, title: item.title }))}
        />
        <div style={{ marginTop: 24 }}>{steps[current].content}</div>
      </>
    </WhiteSectionsPage>
  );
};

export default StepperContainer;
