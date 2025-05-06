import { useEffect, useRef, useState } from "react";
import { CompraInterface, comprarDefault, DetalleCompra, DetalleCompraDefailt } from "../../interfaces/comprasInterfaces";
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
  const [formDataCompra, setFormDataCompra] = useState<CompraInterface>(comprarDefault);
  const [formDataDetalleCompra, setFormDataDetalleCompra] = useState<DetalleCompra>(DetalleCompraDefailt);
  const toastRef = useRef<CustomToastRef>(null);
  const [agregarProductos, setAgregarProductos] = useState(false)
  const [compraId, setCompraId] = useState<string>();
  const navigate = useNavigate();

  const handleChangeCompra = (e: any) => {
    setFormDataCompra({ ...formDataCompra, [e.target.name]: e.target.value });
  };

  const handleChangeDetalleCompra = (e: any) => {
    setFormDataDetalleCompra({ ...formDataDetalleCompra, [e.target.name]: e.target.value });
  };


  // useEffect(() => {
  //   fetchCompras();
  // }, []);

  // const fetchCompras = async () => {
  //   try {
  //     const response = await getAllEmpresas();
  //     if (response) {
  //       // Mezcla el objeto default con lo que venga de la API en caso de que algun campo venga vacio
  //       setFormData({
  //         ...RequestEmpresaDefault,
  //         ...response[0],
  //       });
  //       setCompraId(response[0].id);
  //     }
  //   } catch (error) {
  //     console.log(error);
  //   }
  // };

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

  const handleSendFormCompra = async () => {
    try {
      setAgregarProductos(true)
      const response = await addCompra(formDataCompra)
      console.log(response)
      handleAccion(
        'success',
        <FaCheckCircle size={38} />,
        'proveedor creado con exito'
      );

    } catch (error) {
      setAgregarProductos(false)
      handleAccion(
        'error',
        <IoMdCloseCircle size={38} />,
        'Error al crear el proveedor'
      );
    }
  }

  const steps = [
    {
      title: 'Creación de compra',
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
              className="bg-primary-blue mt-5 rounded-md px-8 py-3 text-white"
              onClick={handleSendFormCompra}
            >
              Crear compra
            </button>
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
            <SteppDetallesProducto
              formData={formDataDetalleCompra}
              handleChange={handleChangeDetalleCompra}
            />
          </div>
          <div className="justify-content-end flex pt-4 gap-3">
            
            <button
              className={`mt-5 rounded-md px-8 py-3 text-white ${!agregarProductos ? 'cursor-not-allowed bg-gray-500' : 'cursor-pointer border border-gray-500 text-gray-500 bg-white'}`}
              onClick={() => { setCurrent(current + 1) }}
              disabled={!agregarProductos}
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
