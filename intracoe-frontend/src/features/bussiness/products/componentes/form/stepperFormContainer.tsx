import React, { useState } from 'react'
import { WhiteSectionsPage } from '../../../../../shared/containers/whiteSectionsPage';
import { Steps } from 'antd';
import { productoInicial, ProductoRequest } from '../../../../../shared/interfaces/interfaces';

export const StepperForm = () => {
  // Estado para controlar el paso actual
  const [current, setCurrent] = useState(0);
  const [formData, setFormData] = useState<ProductoRequest>(productoInicial);

  const handleSendForm = async (e: React.FormEvent) => {
    console.log(e)
  }

  const steps = [
    {
      title: 'Configurar factura',
      content: (
        <>
          <div>
            <p>paso 1</p>
          </div>
          <div className="justify-content-end flex pt-4">
            <button onClick={() => setCurrent(current + 1)}>
              Siguiente
            </button>
          </div>
        </>
      ),
    },
    {
      title: 'Información de contacto',
      content: (
        <>
          <>
            <p>Paso 2</p>
          </>
          <div className="flex w-full justify-between pt-4">
            <button onClick={() => setCurrent(current - 1)}>Atras</button>
            <button onClick={handleSendForm}>
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
        <Steps current={current} items={steps.map((item) => ({ key: item.title, title: item.title }))} />
        <div style={{ marginTop: 24 }}>
          {steps[current].content}
        </div>
      </>
    </WhiteSectionsPage>
  );
}
