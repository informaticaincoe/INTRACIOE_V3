import React, { useState } from 'react';
import { WhiteSectionsPage } from '../../../../../shared/containers/whiteSectionsPage';
import { Steps } from 'antd';
import {
  productoInicial,
  ProductoRequest,
} from '../../../../../shared/interfaces/interfaces';
import { StepperInformacionGeneral } from './stepperInformacionGeneral';
import { StepperFormImpuestoStock } from './stepperFormImpuestoStock';

export const StepperForm = () => {
  // Estado para controlar el paso actual
  const [current, setCurrent] = useState(0);
  const [formData, setFormData] = useState<ProductoRequest>(productoInicial);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSendForm = async (e: React.FormEvent) => {
    console.log(e);
  };

  const steps = [
    {
      title: 'Información general',
      content: (
        <>
          <div>
            <StepperInformacionGeneral
              formData={formData}
              setFormData={setFormData}
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
            <p>Paso 32</p>
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
