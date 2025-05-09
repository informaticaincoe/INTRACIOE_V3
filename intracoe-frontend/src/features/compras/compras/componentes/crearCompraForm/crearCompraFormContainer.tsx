import { useEffect, useRef, useState } from 'react';
import {
  CompraPayload,
  CompraPayloadDeafult,
  DetalleCompraPayload,
  erroresCompra,
} from '../../interfaces/comprasInterfaces';
import CustomToast, {
  CustomToastRef,
  ToastSeverity,
} from '../../../../../shared/toast/customToast';
import { Steps } from 'primereact/steps';
import { SteppCrearCompra } from './steppCrearCompra';
import { useNavigate, useParams } from 'react-router';
import { SteppListaProducto } from './steppListaProductos';
import {
  addCompra,
  getComprasById,
  getDetalleCompras,
  updateComprasById,
} from '../../services/comprasServices';
import { FaCheckCircle } from 'react-icons/fa';
import { IoMdCloseCircle } from 'react-icons/io';

export const CrearCompraFormContainer = () => {
  let { id } = useParams();
  // Estado para controlar el paso actual
  const [current, setCurrent] = useState(0);
  const [formDataCompra, setFormDataCompra] =
    useState<CompraPayload>(CompraPayloadDeafult);
  const [detallesCompra, setDetallesCompra] = useState<DetalleCompraPayload[]>(
    []
  );
  const [errorsCompra, setErrorsCompra] = useState(erroresCompra);
  const toastRef = useRef<CustomToastRef>(null);
  const navigate = useNavigate();

  const handleChangeCompra = (e: any) => {
    console.log('EEEEEEEEEEEEE', e);
    setFormDataCompra({ ...formDataCompra, [e.target.name]: e.target.value });
  };

  useEffect(() => {
    if (id) {
      fetchEditData();
    }
  }, []);

  const fetchEditData = async () => {
    if (id) {
      try {
        const response = await getComprasById(id);
        console.log('COMPAS', response);
        setFormDataCompra(response);
      } catch (error) {
        console.log(error);
      }
    }
    if (id) {
      try {
        const response = await getDetalleCompras(id);
        console.log('DETALLES', response);
        setDetallesCompra(response);
        if (response) {
          const detallesConPre = response.map(det => ({
            ...det,
            preunitario: det.precio_unitario
          }));
          setDetallesCompra(detallesConPre);
        }
      } catch (error) {
        console.log(error);
      }
    }
  };

  useEffect(() => {
    setFormDataCompra({ ...formDataCompra, total: '0' });
  }, [detallesCompra]);

  const moveToStepp2 = () => {
    setCurrent(current + 1);
  };

  const handleSubmit = async () => {
    let newErrors = { proveedor: '', estado: '' };

    if (!formDataCompra.proveedor) {
      newErrors.proveedor = 'Proveedor es un campo requerido';
    }
    if (!formDataCompra.estado) {
      newErrors.estado = 'Estado es un campo requerido';
    }

    setErrorsCompra(newErrors);

    if (!newErrors.proveedor && !newErrors.estado) {
      const data: CompraPayload = {
        ...formDataCompra,
        detalles: detallesCompra,
      };

      console.log('Data que se enviará:', JSON.stringify(data, null, 2));

      // if (id) {
      //   try {
      //     const response = await updateComprasById(id, data);
      //     console.log('Respuesta del backend:', response);

      //     handleAccion(
      //       'success',
      //       <FaCheckCircle />,
      //       'Compra editada correctamente'
      //     );

      //     setTimeout(() => {
      //       navigate('/compras/');
      //     }, 2000);
      //   } catch (error) {
      //     console.error('Error al editar compra:', error);
      //     handleAccion('error', <IoMdCloseCircle />, 'Error al editar la compra');
      //   }
      // } else {
      //   try {
      //     const response = await addCompra(data);
      //     console.log('Respuesta del backend:', response);

      //     handleAccion(
      //       'success',
      //       <FaCheckCircle />,
      //       'Compra creada correctamente'
      //     );

      //     setTimeout(() => {
      //       navigate('/compras/');
      //     }, 2000);
      //   } catch (error) {
      //     console.error('Error al crear compra:', error);
      //     handleAccion('error', <IoMdCloseCircle />, 'Error al crear la compra');
      //   }
      // }
    }
  };

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

  const steps = [
    {
      title: 'Creación de compra',
      content: (
        <>
          <div>
            <SteppListaProducto
              detalles={detallesCompra}
              setDetalles={setDetallesCompra}
            />
          </div>
          <div className="justify-content-end flex gap-3 pt-4">
            <button
              className={`text-primary-blue border-primary-blue bg-white'} mt-5 cursor-pointer rounded-md border px-8 py-3`}
              onClick={moveToStepp2}
            >
              Siguiente
            </button>
          </div>
        </>
      ),
    },
    {
      title: 'Detalles de compra',
      content: (
        <>
          <div>
            <SteppCrearCompra
              formData={formDataCompra}
              handleChange={handleChangeCompra}
              errorCompra={errorsCompra}
            />
          </div>
          <div className="justify-content-end flex gap-3 pt-4">
            <button
              className={`text-primary-blue border-primary-blue mt-5 rounded-md border px-8 py-3`}
              onClick={() => {
                setCurrent(current - 1);
              }}
            >
              Anterior
            </button>
            <button
              className={`bg-primary-blue mt-5 rounded-md px-8 py-3 text-white`}
              onClick={handleSubmit}
            >
              Crear Compra
            </button>
          </div>
        </>
      ),
    },
  ];

  return (
    <>
      <>
        <Steps
          activeIndex={current}
          model={steps.map((item) => ({
            label: item.title,
            key: item.title,
          }))}
          style={{ marginBottom: '5%' }}
          onSelect={(e) => setCurrent(e.index)} // Update the `current` state on step change
        />
        <div style={{ marginTop: 24 }}>{steps[current].content}</div>
        <CustomToast ref={toastRef} />
      </>
    </>
  );
};
