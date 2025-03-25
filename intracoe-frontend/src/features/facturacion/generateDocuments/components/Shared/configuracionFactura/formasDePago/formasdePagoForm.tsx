import { MouseEvent, useEffect, useState } from 'react';
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
import { FaXmark } from "react-icons/fa6";

interface FormasdePagoFormProps {
  formasPagoList: any,
  setFormasPagoList: any
}

export const FormasdePagoForm: React.FC<FormasdePagoFormProps> = ({ formasPagoList, setFormasPagoList }) => {
  const [listFormasdePago, setListFormasdePago] = useState<PaymentMethodInteface[]>([]);
  const [paymentSelected, setPaymentSelected] = useState<PaymentMethodInteface>();
  const [plazosList, setPlazosList] = useState<any[]>([]);
  const [selectedPlazosList, setSelectedPlazosList] = useState<number>(1);
  const [infoPagoLista, setInfoPagoLista] = useState<any[]>([]);

  const [formData, setFormData] = useState({
    id: 0,
    idTipoPago: 0,
    montoPago: 0,
    referecia: "",
    periodo: 0,
    plazo: {},
  });

  useEffect(() => {
    const aux = 
      infoPagoLista.map(pago => {
        return {
          codigo: pago.codigo,  // Solo incluimos el campo 'codigo'
        };
      });
    console.log("aux", aux);
    setFormasPagoList(aux);  // Asignamos solo los objetos con 'codigo'
  }, [infoPagoLista]);
  

  useEffect(() => {
    fetchFormasDePagoList();
    fetchPlazoList();
  }, []);

  const fetchFormasDePagoList = async () => {
    const response = await getAllMetodosDePago()
    setListFormasdePago(response);
  };

  const fetchPlazoList = () => {
    setPlazosList(plazosListTemp);
    if (plazosListTemp && plazosListTemp.length > 0) {
      // Establecer el valor del primer item, no el objeto completo
      setSelectedPlazosList(plazosListTemp[0].codigo);
    }
  };

  const handleChange = (e: InputNumberValueChangeEvent | React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const onClick = () => {
    if (paymentSelected) {
      setInfoPagoLista((prevState) => [
        ...prevState,
        {
          ...formData,
          idTipoPago: paymentSelected.id,
          codigo: paymentSelected.codigo,
          descripcion: paymentSelected.descripcion,
          id: new Date().getTime()
        },
      ]);
    }

    // limpiar formulario
    setFormData({ id: 0, idTipoPago: 0, montoPago: 0, referecia: "", periodo: 0, plazo: {} });
  };

  const deleteFromList = (e: any) => {
    console.log(e);
  
    // Filtra la lista infoPagoLista para eliminar el item cuyo id coincide con e.id
    setInfoPagoLista(infoPagoLista.filter((pago) => pago.id !== e.id));
  };
  
  return (
    <div className="flex w-full flex-col items-start">
      <p className="text-start opacity-70">Métodos de pago</p>
      <div className="flex w-full">
        <div className="w-full">
          <div className='w-full'>
            <Dropdown
              value={paymentSelected}
              onChange={(e: MultiSelectChangeEvent) =>
                setPaymentSelected(e.value)
              }
              options={listFormasdePago}
              optionLabel="descripcion"
              placeholder="Seleccionar metodo de pago"
              className="w-full text-start"
              filter
            />
          </div>
          {/* Formulario pagos */}
          {
            paymentSelected && (
              <section className="grid w-full grid-cols-2 gap-5 mt-5">
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
                        />
                      </div>
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
                    <button className="border-primary-blue text-primary-blue w-full rounded-md border py-2">
                      Limpiar
                    </button>
                    <button
                      className="bg-primary-blue w-full rounded-md py-2 text-white"
                      onClick={onClick}
                    >
                      Añadir
                    </button>
                  </span>
                </div>
                {infoPagoLista && infoPagoLista.length > 0 && (
                  <div className="grid grid-cols-2 gap-5 auto-rows-min" key={new Date().getTime()}>
                    {infoPagoLista.map((pago, index) => {
                      <button ></button>
                      return (
                        <div className='relative border border-border-color rounded-md'>
                          <button className="absolute right-0 px-5 py-4 hover:text-gray hover:cursor-pointer" onClick={() => deleteFromList(pago)}><FaXmark className='text-border-color' /></button>
                          <div className=" flex text-center gap-2 py-4 flex-col items-center justify-center" key={index}>
                            <p className='opacity-70 '>{pago.descripcion}</p> {/* Asegúrate de usar el campo correcto */}
                            <p className='font-semibold text-2xl'>$ {pago.montoPago}</p> {/* Asegúrate de usar el campo correcto */}
                            <p className='opacity-70'>{pago.referecia}</p> {/* Asegúrate de usar el campo correcto */}
                          </div>
                        </div>
                      );
                    })}
                  </div>
                )}
              </section>
            )
          }
        </div>
      </div>
    </div>
  );
};
