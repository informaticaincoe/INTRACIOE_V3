import React, { useEffect, useRef, useState } from 'react'
import { WhiteSectionsPage } from '../../../../../shared/containers/whiteSectionsPage';
import { Steps } from 'antd';
import CustomToast, { CustomToastRef, ToastSeverity } from '../../../../../shared/toast/customToast';
import { useParams } from 'react-router';
import { RequestEmpresa, RequestEmpresaDefault } from '../../../../../shared/interfaces/interfaces';
import { StepperConfiguracionFacturacion } from './stepperConfiguracionFacturacion';
import { StepperContactBussiness } from './stepperContactBussiness';
import { createEmpresa, editReceptor, getAllEmpresas } from '../../services/empresaServices';

export const FormConfigBussinessContainer = () => {
  let params = useParams()

  // Estado para controlar el paso actual
  const [current, setCurrent] = useState(0);
  const [formData, setFormData] = useState<RequestEmpresa>(RequestEmpresaDefault);
  const toastRef = useRef<CustomToastRef>(null);
  const [empresaId, setEmpresaId] = useState<string>()
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  useEffect(() => {
    fetchEmpresa()
  }, [])

  const fetchEmpresa = async () => {
    try {
      const response = await getAllEmpresas()
      if (response) {
        // Mezcla el objeto default con lo que venga de la API en caso de que algun campo venga vacio
        setFormData({
          ...RequestEmpresaDefault,
          ...response[0],
        });
        setEmpresaId(response[0].id);
      }
    } catch (error) {
      console.log(error)
    }
  }

  // const fetchReceptorEdit = async () => {
  //     try {
  //         if (params.id) {
  //             const data = await getReceptorById(params.id)
  //             console.log(data)
  //             setFormData(data)
  //         }
  //     } catch (error) {
  //         console.log(error)
  //     }
  // }

  // const handleAccion = (
  //     severity: ToastSeverity,
  //     icon: any,
  //     summary: string
  // ) => {
  //     toastRef.current?.show({
  //         severity: severity,
  //         summary: summary,
  //         icon: icon,
  //         life: 2000,
  //     });
  // };

  const handleSendForm = async (e: React.FormEvent) => {
    e.preventDefault();

    console.log('=== FormData ===');
    Object.entries(formData).forEach(([key, value]) => {
      console.log(`${key}:`, JSON.stringify(value, null, 2));
    });
    console.log('================');

    console.log(formData)
    if (empresaId) {
      try {
          const response = await editReceptor(empresaId, formData);
          console.log(response);
      } catch (error) {
          console.log(error);
      }
    }
    else {
      try {
        const response = await createEmpresa(formData);
        console.log(response);
      } catch (error) {
        console.log(error);
      }
    }
  };

  const steps = [
    {
      title: 'Información general',
      content: (
        <>
          <div>
            <StepperConfiguracionFacturacion
              formData={formData}
              handleChange={handleChange}
            />
          </div>
          <div className="justify-content-end flex pt-4">
            <button
              className='bg-primary-blue text-white px-8 py-3 mt-5 rounded-md'
              onClick={() =>
                setCurrent(current + 1)}
            >
              Siguiente
            </button>
          </div>
        </>
      ),
    },
    {
      title: 'informacion de contacto',
      content: (
        <>
          <StepperContactBussiness
            formData={formData}
            handleChange={handleChange}
          />
          <div className="flex w-full justify-between pt-4">
            <button
              onClick={() => setCurrent(current - 1)}
              className="border-gray text-gray rounded-md border px-10 py-3"
            >
              Atras
            </button>
            <button
              className="bg-primary-yellow rounded-md px-6 py-3 text-white"
              onClick={handleSendForm}
            >
              Guardar
            </button>
          </div>
        </>
      ),
    },
  ];

  return (
    <>
      <WhiteSectionsPage className="mx-[10%] px-[5%] py-[3%]">
        <>
          <Steps
            current={current}
            items={steps.map((item) => ({ key: item.title, title: item.title }))}
            style={{ marginBottom: '5%' }}
          />
          <div style={{ marginTop: 24 }}>{steps[current].content}</div>
          <CustomToast ref={toastRef} />
        </>
      </WhiteSectionsPage>
    </>
  );
};
