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

export const StepperForm = () => {
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

    // 1) Creamos el FormData
    const payload = new FormData();

    // Campos simples
    payload.append('codigo', formData.codigo);
    payload.append('descripcion', formData.descripcion);
    payload.append('preunitario', formData.preunitario.toString());
    payload.append('precio_compra', formData.precio_compra.toString());
    payload.append('precio_venta', formData.precio_venta.toString());
    payload.append('stock', formData.stock.toString());
    payload.append('stock_minimo', formData.stock_minimo.toString());
    payload.append('stock_maximo', formData.stock_maximo.toString());
    payload.append('tributo', formData.tributo.toString());
    payload.append('precio_iva', formData.precio_iva ? 'true' : 'false');
    payload.append('maneja_lotes', formData.maneja_lotes ? 'true' : 'false');

    // Relaciones opcionales
    if (formData.categoria != null) {
      // si categoria es un número
      if (typeof formData.categoria === 'number') {
        payload.append('categoria', formData.categoria);
      } else {
        // si es un objeto con id
        payload.append('categoria', (formData.categoria as any).id.toString());
      }
    }
    if (formData.unidad_medida != null) {
      payload.append('unidad_medida', formData.unidad_medida.toString());
    }
    if (formData.tipo_item != null) {
      payload.append('tipo_item', formData.tipo_item.toString());
    }
    if (formData.referencia_interna) {
      payload.append('referencia_interna', formData.referencia_interna);
    }

    // Arrays: impuestos y almacenes
    formData.impuestos?.forEach(id => {
      payload.append('impuestos', id.toString());
    });
    formData.almacenes.forEach(id => {
      payload.append('almacenes', id.toString());
    });
    if (formData.fecha_vencimiento) {
      // Forzamos a string (quita cualquier guión bajo o espacio sobrante)
      const fechaStr = String(formData.fecha_vencimiento).trim().replace(/_+$/, '');
      payload.append('fecha_vencimiento', fechaStr);
    }

    // 2) Imagen (File)
    if (formData.imagen instanceof File) {
      payload.append('imagen', formData.imagen, formData.imagen.name);
    }


    try {
      // 3) Envío con axios (o tu fetch), sin especificar Content-Type
      if (params.id) {
        const response = await EditProductService(params.id, payload);

      }
      else {
        const response = await createProductService(payload);

      }
      handleAccion(
        'success',
        <FaCheckCircle size={38} />,
        'Producto guardado con exito'
      );

      setTimeout(() => {
        navigate('/productos/')
      }, 2000)


    } catch (err) {
      handleAccion(
        'error',
        <IoMdCloseCircle size={38} />,
        'Ha ocurrido un error al guardar el producto'
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
