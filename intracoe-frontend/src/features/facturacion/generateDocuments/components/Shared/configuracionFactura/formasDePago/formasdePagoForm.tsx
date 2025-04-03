import { useEffect, useRef, useState } from 'react';
import { PaymentMethodInteface } from './formasdePagoData';
import { Dropdown } from 'primereact/dropdown';
import { FaRegCreditCard } from 'react-icons/fa6';
import { MultiSelectChangeEvent } from 'primereact/multiselect';
import {
  InputNumber,
  InputNumberValueChangeEvent,
} from 'primereact/inputnumber';
import { plazosListTemp } from '../plazos';
import styles from './formasDePagoCustom.module.css';
import { getAllMetodosDePago } from '../../../../services/configuracionFactura/configuracionFacturaService';
import { InputText } from 'primereact/inputtext';
import { FaXmark } from 'react-icons/fa6';
import CustomToast, {
  CustomToastRef,
  ToastSeverity,
} from '../../../../../../../shared/toast/customToast';
import { IoMdCloseCircle } from 'react-icons/io';

interface FormasdePagoFormProps {
  setFormasPagoList: any;
  totalAPagar: number;
  setErrorFormasPago: any;
  errorFormasPago: boolean;
  setAuxManejoPagos: any;
  auxManejoPagos: any;
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
    id: 0,
    idTipoPago: 0,
    montoPago: 0,
    referecia: '',
    periodo: 0,
    plazo: {},
  });
  const toastRef = useRef<CustomToastRef>(null);

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

  useEffect(() => {
    const aux = infoPagoLista.map((pago) => {
      return pago.codigo; // Solo incluimos el campo 'codigo'
    });
    setFormasPagoList(aux); // Asignamos solo los objetos con 'codigo'
  }, [infoPagoLista]);

  useEffect(() => {
    fetchFormasDePagoList();
    fetchPlazoList();
  }, []);

  useEffect(() => {
    setAuxManejoPagos(totalAPagar);
  }, [totalAPagar]);

  const fetchFormasDePagoList = async () => {
    const response = await getAllMetodosDePago();
    setListFormasdePago(response);
  };

  const fetchPlazoList = () => {
    setPlazosList(plazosListTemp);
    if (plazosListTemp && plazosListTemp.length > 0) {
      // Establecer el valor del primer item, no el objeto completo
      setSelectedPlazosList(plazosListTemp[0].codigo);
    }
  };

  const handlePagoCompleto = () => {
    setFormData({ ...formData, montoPago: auxManejoPagos });
  };

  const handleChange = (
    e: InputNumberValueChangeEvent | React.ChangeEvent<HTMLInputElement>
  ) => {
    const newValue = Number(e.target.value);
    setFormData({ ...formData, [e.target.name]: newValue });
  };

  const onClick = () => {
    if (paymentSelected) {
      // Verifica si requiere referencia y está vacía
      if (paymentSelected.codigo !== '01' && !formData.referecia) {
        setErrorFormasPago(true);
        setErorReferencia(true);
        return;
      }

      // Verifica monto válido
      if (formData.montoPago <= auxManejoPagos) {
        setInfoPagoLista((prevState) => [
          ...prevState,
          {
            ...formData,
            idTipoPago: paymentSelected.id,
            codigo: paymentSelected.codigo,
            descripcion: paymentSelected.descripcion,
            id: new Date().getTime(),
          },
        ]);
        setAuxManejoPagos(
          Math.round((auxManejoPagos - formData.montoPago) * 100) / 100
        );
        if (auxManejoPagos - formData.montoPago == 0 && errorFormasPago)
          setErrorFormasPago(false);
      } else {
        handleAccion(
          'error',
          <IoMdCloseCircle size={38} />,
          'El monto a pagar es mayor al total de la factura'
        );
      }

      // Resetear el formulario
      setFormData({
        id: 0,
        idTipoPago: 0,
        montoPago: 0,
        referecia: '',
        periodo: 0,
        plazo: {},
      });
      setErorReferencia(false); // resetea error de referencia
    }
  };

  const deleteFromList = (e: any) => {
    setAuxManejoPagos(auxManejoPagos + e.montoPago);
    // Filtra la lista infoPagoLista para eliminar el item cuyo id coincide con e.id
    setInfoPagoLista(infoPagoLista.filter((pago) => pago.id !== e.id));
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
                        optionLabel="valor"
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
