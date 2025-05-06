import { useEffect, useRef, useState } from "react";
import { CompraInterface, CompraPayload, CompraPayloadDeafult, comprarDefault, DetalleCompra, DetalleCompraDefault } from "../../interfaces/comprasInterfaces";
import CustomToast, { CustomToastRef, ToastSeverity } from "../../../../../shared/toast/customToast";
import { WhiteSectionsPage } from "../../../../../shared/containers/whiteSectionsPage";
import { Steps } from "primereact/steps";
import { SteppCrearCompra } from "./steppCrearCompra";
import { addCompra } from "../../services/comprasServices";
import { FaCheckCircle } from "react-icons/fa";
import { useNavigate } from "react-router";
import { IoMdCloseCircle } from "react-icons/io";
import { SteppDetallesProducto } from "./steppDetallesProductos";


export const CrearCompraFormContainer = () => {
  // Estado para controlar el paso actual
  const [current, setCurrent] = useState(0);
  const [formDataCompra, setFormDataCompra] = useState<CompraPayload>(CompraPayloadDeafult);
  const [formDataDetalleCompra, setFormDataDetalleCompra] = useState<DetalleCompra>(DetalleCompraDefault);
  const toastRef = useRef<CustomToastRef>(null);
  const [agregarProductos, setAgregarProductos] = useState(false)
  const navigate = useNavigate();

  const handleChangeCompra = (e: any) => {
    setFormDataCompra({ ...formDataCompra, [e.target.name]: e.target.value });
  };

  const handleChangeDetalleCompra = (e: any) => {
    setFormDataDetalleCompra({ ...formDataDetalleCompra, [e.target.name]: e.target.value });
  };

  const handleSubmit = async () => {
    console.log("Se hizo click en CREAR");

    const data: CompraPayload = {
      ...formDataCompra,
      detalles: [formDataDetalleCompra],
    };

    console.log("Data que se enviará:", JSON.stringify(data, null, 2));


    try {
      const response = await addCompra(data); // <-- ENVÍA TODO
      console.log("Respuesta del backend:", response);

      handleAccion("success", <FaCheckCircle />, "Compra creada correctamente");

      setTimeout(() => {
        navigate('/compras/');
      }, 2000);

    } catch (error) {
      console.error("Error al crear compra:", error);
      handleAccion("error", <IoMdCloseCircle />, "Error al crear la compra");
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
            <SteppDetallesProducto
              formData={formDataDetalleCompra}
              handleChangeDetalle={handleChangeDetalleCompra}
            />

          </div>
          <div className="justify-content-end flex pt-4 gap-3">
            <button
              className={`mt-5 rounded-md px-8 py-3 text-white ${!agregarProductos ? 'cursor-not-allowed bg-gray-500' : 'cursor-pointer border border-gray-500 text-gray-500 bg-white'}`}
              onClick={() => { setCurrent(current + 1) }}
              disabled={agregarProductos}
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
            />
          </div>
          <div className="justify-content-end flex pt-4 gap-3">
            <button
              className={`mt-5 rounded-md px-8 py-3 text-primary-blue `}
              onClick={() => { setCurrent(current - 1) }}
            >
              Anterior
            </button>
            <button
              className={`mt-5 rounded-md px-8 py-3 text-primary-blue `}
              onClick={handleSubmit}
            >
              Crear
            </button>
          </div>
        </>
      ),
    },
  ];

  return (
    <>
      <WhiteSectionsPage >
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
      </WhiteSectionsPage>
    </>
  );
};
