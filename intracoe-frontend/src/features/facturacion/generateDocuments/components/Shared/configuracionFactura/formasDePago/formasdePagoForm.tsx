import { useEffect, useRef, useState } from 'react';
import { Dropdown } from 'primereact/dropdown';
import {
  InputNumber,
  InputNumberValueChangeEvent,
} from 'primereact/inputnumber';
import { InputText } from 'primereact/inputtext';
import { FaRegCreditCard } from 'react-icons/fa6';
import { FaXmark } from 'react-icons/fa6';
import { IoMdCloseCircle } from 'react-icons/io';
import CustomToast, {
  CustomToastRef,
  ToastSeverity,
} from '../../../../../../../shared/toast/customToast';
import styles from './formasDePagoCustom.module.css';
import { MultiSelectChangeEvent } from 'primereact/multiselect';
import { PaymentMethodInteface } from './formasdePagoData';
import {
  getAllMetodosDePago,
  getAllPlazos,
} from '../../../../../../../shared/catalogos/services/catalogosServices';

interface FormasdePagoFormProps {
  setFormasPagoList: (codes: string[]) => void;
  totalAPagar: number;
  setErrorFormasPago: (b: boolean) => void;
  errorFormasPago: boolean;
  setAuxManejoPagos: (n: number) => void;
  auxManejoPagos: number;
}

export const FormasdePagoForm: React.FC<FormasdePagoFormProps> = ({
  setFormasPagoList,
  totalAPagar,
  setErrorFormasPago,
  errorFormasPago,
  setAuxManejoPagos,
  auxManejoPagos,
}) => {
  const [listFormasdePago, setListFormasdePago] = useState<
    PaymentMethodInteface[]
  >([]);
  const [paymentSelected, setPaymentSelected] =
    useState<PaymentMethodInteface>();
  const [plazosList, setPlazosList] = useState<any[]>([]);
  const [selectedPlazosList, setSelectedPlazosList] = useState<number>(1);
  const [infoPagoLista, setInfoPagoLista] = useState<any[]>([]);
  const [erorReferencia, setErorReferencia] = useState<boolean>(false);
  const [formData, setFormData] = useState({
    montoPago: 0,
    referecia: '',
    periodo: 0,
  });
  const toastRef = useRef<CustomToastRef>(null);

  const handleAccion = (
    severity: ToastSeverity,
    icon: any,
    summary: string
  ) => {
    toastRef.current?.show({ severity, summary, icon, life: 2000 });
  };

  useEffect(() => {
    getAllMetodosDePago().then(setListFormasdePago);
    fetchPlazos();
  }, []);

  const fetchPlazos = async () => {
    try {
      const response = await getAllPlazos();
      setPlazosList(response);
      setSelectedPlazosList(response[0].codigo);
    } catch (error) {
      console.log(error);
    }
  };

  // Cada vez que cambie la lista de pagos o el total, recalcula remaining
  useEffect(() => {
    const pagado = infoPagoLista.reduce((sum, p) => sum + p.montoPago, 0);
    let remaining = Math.round((totalAPagar - pagado) * 100) / 100;

    if (remaining < 0) {
      // Si queda negativo, resetea todo
      setInfoPagoLista([]);
      remaining = totalAPagar;
    }

    setAuxManejoPagos(remaining);
    // También actualiza los códigos en el padre
    setFormasPagoList(infoPagoLista.map((p) => p.codigo));
  }, [infoPagoLista, totalAPagar, setAuxManejoPagos, setFormasPagoList]);

  const handleChange = (
    e: InputNumberValueChangeEvent | React.ChangeEvent<HTMLInputElement>
  ) => {
    const { name, value } = e.target as any;
    setFormData((fd) => ({ ...fd, [name]: Number(value) }));
  };

  const handlePagoCompleto = () => {
    setFormData((fd) => ({ ...fd, montoPago: auxManejoPagos }));
  };

  const onClick = () => {
    if (!paymentSelected) {
      setErrorFormasPago(true);
      return;
    }
    // referencia obligatoria si no es efectivo
    if (paymentSelected.codigo !== '01' && !formData.referecia) {
      setErrorFormasPago(true);
      setErorReferencia(true);
      return;
    }
    // monto válido
    if (formData.montoPago <= auxManejoPagos) {
      setInfoPagoLista((prev) => [
        ...prev,
        {
          ...formData,
          idTipoPago: paymentSelected.id,
          codigo: paymentSelected.codigo,
          descripcion: paymentSelected.descripcion,
          id: Date.now(),
        },
      ]);
      setErrorFormasPago(false);
      setErorReferencia(false);
      // limpia form
      setFormData({ montoPago: 0, referecia: '', periodo: 0 });
    } else {
      handleAccion(
        'error',
        <IoMdCloseCircle size={38} />,
        'El monto excede el total restante'
      );
    }
  };

  const deleteFromList = (item: any) => {
    setInfoPagoLista((prev) => prev.filter((p) => p.id !== item.id));
  };
  return (
    <div className="flex w-full flex-col items-start">
      <p className="text-start opacity-70">Métodos de pago</p>
      <div className="flex w-full">
        <div className="w-full">
          <div className="w-full">
            <Dropdown
              value={paymentSelected}
              onChange={(e: MultiSelectChangeEvent) =>
                setPaymentSelected(e.value)
              }
              options={listFormasdePago}
              optionLabel="descripcion"
              placeholder="Seleccionar metodo de pago"
              className={`w-full text-start ${errorFormasPago ? 'p-invalid' : ''} `}
              filter
            />
            {errorFormasPago && (
              <p className="text-red text-start">
                Campo formas de pago no debe estar vacio o incompleto
              </p>
            )}
          </div>

          {/* Formulario pagos */}

          {paymentSelected && (
            <section className="mt-5 grid w-full grid-cols-2 gap-5">
              <div className="flex w-[100%] flex-col gap-3 rounded-md border border-gray-200 px-10 py-8">
                <span className="flex flex-col">
                  <label htmlFor="montoPagar" className="text-start opacity-70">
                    Monto a pagar
                  </label>
                  <div className="p-inputgroup flex-1">
                    <span className="p-inputgroup-addon">$</span>
                    <InputNumber
                      name="montoPago"
                      placeholder="Price"
                      value={formData.montoPago}
                      onValueChange={(e: InputNumberValueChangeEvent) =>
                        handleChange(e)
                      }
                    />
                  </div>
                </span>
                {paymentSelected.codigo != '01' && (
                  <span className="flex flex-col">
                    <label
                      htmlFor="referencia"
                      className="text-start opacity-70"
                    >
                      Referencia
                    </label>
                    <div className="p-inputgroup flex-1">
                      <span className="p-inputgroup-addon">
                        <FaRegCreditCard />
                      </span>
                      <InputText
                        name="referecia"
                        placeholder="Número referencia"
                        value={formData.referecia}
                        onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                          handleChange(e)
                        }
                        className={`${erorReferencia && 'p-invalid'}`}
                      />
                    </div>
                    {erorReferencia && (
                      <p className="text-red text-start">Campo obligatorio</p>
                    )}
                  </span>
                )}
                <span className="flex flex-col pb-5">
                  <label htmlFor="periodo" className="text-start opacity-70">
                    Periodo
                  </label>
                  <div className="p-inputgroup flex-1">
                    <span className="p-inputgroup-addon">
                      <FaRegCreditCard />
                    </span>
                    <InputNumber
                      name="periodo"
                      placeholder="1"
                      value={formData.periodo}
                      onValueChange={(e: InputNumberValueChangeEvent) =>
                        handleChange(e)
                      }
                    />
                    <span className="p-inputgroup-addon">
                      <Dropdown
                        value={selectedPlazosList}
                        onChange={(e: { value: any }) =>
                          setSelectedPlazosList(e.value)
                        }
                        options={plazosList}
                        optionLabel="descripcion"
                        optionValue="codigo"
                        placeholder="Seleccionar tipo de plazo"
                        className={`md:w-14rem font-display flex w-full gap-2 bg-none text-start text-nowrap ${styles.inputWrapper}`}
                      />
                    </span>
                  </div>
                </span>
                <span className="flex justify-between gap-5">
                  <button
                    className="border-primary-blue text-primary-blue w-full rounded-md border py-2"
                    onClick={handlePagoCompleto}
                  >
                    Pago completo
                  </button>
                  <button
                    className={`"bg-primary-blue w-full rounded-md py-2 text-white ${auxManejoPagos == 0 ? 'bg-gray cursor-not-allowed' : 'bg-primary-blue'}`}
                    onClick={onClick}
                    disabled={auxManejoPagos == 0}
                  >
                    Añadir
                  </button>
                </span>
                <p className="pt-5 text-start">
                  Falta a pagar: $ {Math.round(auxManejoPagos * 100) / 100}
                </p>
              </div>

              {infoPagoLista && infoPagoLista.length > 0 && (
                <div className="grid auto-rows-min grid-cols-2 gap-5">
                  {infoPagoLista.map((pago, index) => {
                    return (
                      <div
                        className="border-border-color relative rounded-md border"
                        key={index}
                      >
                        <button
                          className="hover:text-gray absolute right-0 px-5 py-4 hover:cursor-pointer"
                          onClick={() => deleteFromList(pago)}
                        >
                          <FaXmark className="text-border-color" />
                        </button>
                        <div
                          className="flex flex-col items-center justify-center gap-2 py-4 text-center"
                          key={index}
                        >
                          <p className="opacity-70">{pago.descripcion}</p>{' '}
                          {/* Asegúrate de usar el campo correcto */}
                          <p className="text-2xl font-semibold">
                            $ {parseFloat(pago.montoPago)}
                          </p>{' '}
                          {/* Asegúrate de usar el campo correcto */}
                          <p className="opacity-70">{pago.referecia}</p>{' '}
                          {/* Asegúrate de usar el campo correcto */}
                        </div>
                      </div>
                    );
                  })}
                </div>
              )}
            </section>
          )}
        </div>
      </div>
      <CustomToast ref={toastRef} />
    </div>
  );
};
