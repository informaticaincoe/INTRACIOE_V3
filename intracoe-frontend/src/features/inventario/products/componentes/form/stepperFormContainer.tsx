import React, { useEffect, useRef, useState } from 'react';
import { WhiteSectionsPage } from '../../../../../shared/containers/whiteSectionsPage';
import { Steps } from 'antd';
import {
  productoInicial,
  ProductoRequest,
} from '../../../../../shared/interfaces/interfaces';
import { StepperInformacionGeneral } from './stepperInformacionGeneral';
import { StepperFormImpuestoStock } from './stepperFormImpuestoStock';
import { StepperFormLotesYVencimiento } from './stepperFormLotesYVencimiento';
import { createProductService, EditProductService, getProductById } from '../../services/productsServices';
import CustomToast, { CustomToastRef, ToastSeverity } from '../../../../../shared/toast/customToast';
import { IoMdCloseCircle } from 'react-icons/io';
import { FaCheckCircle } from "react-icons/fa";
import { useNavigate, useParams } from 'react-router';

export const StepperFormContainer = () => {
  let params = useParams()

  // Estado para controlar el paso actual
  const [current, setCurrent] = useState(0);
  const [formData, setFormData] = useState<ProductoRequest>(productoInicial);
  const toastRef = useRef<CustomToastRef>(null);
  const navigate = useNavigate()

  useEffect(() => {
    if (params.id) {
      fetchProductDataEdit()
    }
  }, [])

  const fetchProductDataEdit = async () => {
    try {
      if (params.id) {
        const data = await getProductById(params.id)
        setFormData(data)
      }
    } catch (error) {
      console.log(error)
    }
  }

  const handleAccion = (
    severity: ToastSeverity,
    icon: any,
    summary: string
  ) => {
    toastRef.current?.show({
      severity: severity,
      summary: summary,
      icon: icon,
      life: 2000,
    });
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSendForm = async (e: React.FormEvent) => {
    e.preventDefault();
    console.log("data-----", formData.imagen)
    console.log("datatypeof-----", typeof (formData.imagen))

    try {
      // 3) Envío con axios (o tu fetch), sin especificar Content-Type
      if (params.id) {
        const response = await EditProductService(params.id, formData);

      }
      else {
        const response = await createProductService(formData);

      }
      handleAccion(
        'success',
        <FaCheckCircle size={38} />,
        'Configuracion guardada con exito'
      );

      setTimeout(() => {
        navigate('/productos/')
      }, 2000)


    } catch (err) {
      handleAccion(
        'error',
        <IoMdCloseCircle size={38} />,
        'Ha ocurrido un error al guardar la configuracion'
      );
    }
  };


  const steps = [
    {
      title: 'Información general',
      content: (
        <>
          <div>
            <StepperInformacionGeneral
              formData={formData}
              handleChange={handleChange}
            />
          </div>
          <div className="justify-content-end flex pt-4">
            <button
              onClick={() => setCurrent(current + 1)}
              className="bg-primary-blue rounded-md px-6 py-3 text-white"
            >
              Siguiente
            </button>
          </div>
        </>
      ),
    },
    {
      title: 'impuestos y stock',
      content: (
        <>
          <>
            <StepperFormImpuestoStock
              formData={formData}
              handleChange={handleChange}
            />
          </>
          <div className="flex w-full justify-between pt-4">
            <button
              onClick={() => setCurrent(current - 1)}
              className="border-gray text-gray rounded-md border px-10 py-3"
            >
              Atras
            </button>
            <button
              onClick={() => setCurrent(current + 1)}
              className="bg-primary-blue rounded-md px-6 py-3 text-white"
            >
              Siguiente
            </button>
          </div>
        </>
      ),
    },
    {
      title: 'Lotes y vsencimiento',
      content: (
        <>
          <>
            <StepperFormLotesYVencimiento
              formData={formData}
              handleChange={handleChange}
            />
          </>
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
  );
};
