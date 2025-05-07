import { useEffect, useRef, useState } from "react";
import { CompraInterface, CompraPayload, CompraPayloadDeafult, comprarDefault, DetalleCompra, DetalleCompraDefault, erroresCompra, erroresDetalleCompra } from "../../interfaces/comprasInterfaces";
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
  const [errorsCompra, setErrorsCompra] = useState(erroresCompra);
  const [errorsDetalle, setErrorsDetalle] = useState(erroresDetalleCompra);
  const toastRef = useRef<CustomToastRef>(null);
  const [agregarProductos, setAgregarProductos] = useState(false)
  const navigate = useNavigate();

  const handleChangeCompra = (e: any) => {
    setFormDataCompra({ ...formDataCompra, [e.target.name]: e.target.value });
  };

  const handleChangeDetalleCompra = (e: any) => {
    if (e.target.name == "precio_unitario") {
      console.log("precio_unitario")
      setFormDataDetalleCompra({ ...formDataDetalleCompra, [e.target.name]: e.target.value, 'preunitario': e.target.value });
    }
    else
      setFormDataDetalleCompra({ ...formDataDetalleCompra, [e.target.name]: e.target.value });
  };

  useEffect(()=> {
    const total = parseInt(formDataDetalleCompra.cantidad) * parseFloat(formDataDetalleCompra.precio_unitario)
    setFormDataCompra({ ...formDataCompra, "total": total.toString() });

  },[formDataDetalleCompra.cantidad, formDataDetalleCompra.precio_unitario])

  const moveToStepp2 = () => {
    let newErrors = { codigo: "", descripcion: "", categoria: "", precio_venta: "", cantidad: "", precio_unitario: "", preunitario: "" };


    if (!formDataDetalleCompra.codigo) {
      newErrors.codigo = 'Codigo es un campo requerido';
    }
    if (!formDataDetalleCompra.descripcion) {
      newErrors.descripcion = 'Descripcion es un campo requerido';
    }
    if (!formDataDetalleCompra.cantidad) {
      newErrors.cantidad = 'Cantidad es un campo requerido';
    }
    if (!formDataDetalleCompra.precio_unitario) {
      newErrors.precio_unitario = 'Precio unitario es un campo requerido';
    }
    if (!formDataDetalleCompra.precio_venta) {
      newErrors.precio_venta = 'Precio es un campo requerido';
    }
    setErrorsDetalle(newErrors);
    if (!newErrors.codigo && !newErrors.descripcion && !newErrors.categoria && !newErrors.precio_venta && !newErrors.cantidad && !newErrors.precio_unitario)
      setCurrent(current + 1)
  }

  const handleSubmit = async () => {
    let newErrors = { proveedor: "", estado: "" };

    if (!formDataCompra.proveedor) {
      newErrors.proveedor = 'Proveedor es un campo requerido';
    }
    if (!formDataCompra.estado) {
      newErrors.estado = 'Estado es un campo requerido';
    }

    console.log("errores compra", newErrors)

    setErrorsCompra(newErrors);

    if (!newErrors.proveedor && !newErrors.estado) {
      const data: CompraPayload = {
        ...formDataCompra,
        detalles: [formDataDetalleCompra],
      };

      console.log("Data que se enviará:", JSON.stringify(data, null, 2));

      // try {
      //   const response = await addCompra(data); // <-- ENVÍA TODO
      //   console.log("Respuesta del backend:", response);

      //   handleAccion("success", <FaCheckCircle />, "Compra creada correctamente");

      //   setTimeout(() => {
      //     navigate('/compras/');
      //   }, 2000);

      // } catch (error) {
      //   console.error("Error al crear compra:", error);
      //   handleAccion("error", <IoMdCloseCircle />, "Error al crear la compra");
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
            <SteppDetallesProducto
              formData={formDataDetalleCompra}
              handleChangeDetalle={handleChangeDetalleCompra}
              errorsDetalle={errorsDetalle}
            />
          </div>
          <div className="justify-content-end flex pt-4 gap-3">
            <button
              className={`mt-5 rounded-md px-8 py-3 text-primary-blue cursor-pointer border border-primary-blue bg-white'}`}
              onClick={moveToStepp2}
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
              errorCompra={errorsCompra}
            />
          </div>
          <div className="justify-content-end flex pt-4 gap-3">
            <button
              className={`mt-5 rounded-md px-8 py-3 text-primary-blue border border-primary-blue `}
              onClick={() => { setCurrent(current - 1) }}
            >
              Anterior
            </button>
            <button
              className={`mt-5 rounded-md px-8 py-3 bg-primary-blue text-white`}
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
