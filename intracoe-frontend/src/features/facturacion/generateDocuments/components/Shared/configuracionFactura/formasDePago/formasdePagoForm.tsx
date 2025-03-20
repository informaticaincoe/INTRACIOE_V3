import { useEffect, useState } from 'react';
import { PaymentMethodInteface, paymentMethodsList } from './formasdePagoData';
import { Dropdown } from 'primereact/dropdown';
import { FaRegCreditCard } from 'react-icons/fa6';
import { MultiSelectChangeEvent } from 'primereact/multiselect';
import {
  InputNumber,
  InputNumberValueChangeEvent,
} from 'primereact/inputnumber';
import { plazosListTemp } from '../plazos';
import styles from './formasDePagoCustom.module.css';

export const FormasdePagoForm = () => {
  const [listFormasdePago, setListFormasdePago] = useState<
    PaymentMethodInteface[]
  >([]);
  const [paymentSelected, setPaymentSelected] =
    useState<PaymentMethodInteface>();
  const [plazosList, setPlazosList] = useState<any[]>([]);
  const [selectedPlazosList, setSelectedPlazosList] = useState<number>(1);
  const [guardarListAux, setGuardarListAux] = useState<any[]>([]);

  const [formData, setFormData] = useState({
    montoPago: 0,
    referecia: 0,
    periodo: 0,
    plazo: {},
  });

  useEffect(() => {
    console.log(guardarListAux);
  }, [formData]);

  const handleChange = (e: InputNumberValueChangeEvent) => {
    console.log(e.target.name, e.target.value);
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const onClick = () => {
    if (paymentSelected) {
      setGuardarListAux((prevState) => [
        ...prevState,
        {
          ...formData,
          codigo: paymentSelected.codigo,
          descripcion: paymentSelected.descripcion,
        },
      ]);
    }

    // limpiar formulario
    setFormData({ montoPago: 0, referecia: 0, periodo: 0, plazo: {} });
  };

  useEffect(() => {
    fetchActividadesList();
    fetchPlazoList();
  }, []);

  const fetchActividadesList = () => {
    setListFormasdePago(paymentMethodsList);
  };

  const fetchPlazoList = () => {
    setPlazosList(plazosListTemp);
    if (plazosListTemp && plazosListTemp.length > 0) {
      // Establecer el valor del primer item, no el objeto completo
      setSelectedPlazosList(plazosListTemp[0].codigo);
    }
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
              placeholder="Seleccionar actividad economica"
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
                        <InputNumber
                          name="referecia"
                          placeholder="Price"
                          value={formData.referecia}
                          onValueChange={(e: InputNumberValueChangeEvent) =>
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
                          value={selectedPlazosList} // Esto es solo el valor 'codigo'
                          onChange={(e: { value: any }) =>
                            setSelectedPlazosList(e.value)
                          }
                          options={plazosList}
                          optionLabel="valor" // El texto visible en las opciones
                          optionValue="codigo" // Este es el valor que debe coincidir con 'selectedPlazosList'
                          placeholder="Seleccionar tipo de plazo"
                          className={`md:w-14rem font-display flex w-full gap-2 bg-none text-start text-nowrap ${styles.inputWrapper}`}
                        //FIXME: Revisar estilos para reducir ancho de la lista
                        // pt={{
                        //     panel: {
                        //         className: `${styles.dropdownPanel}`,  // Aplica el estilo personalizado para el panel
                        //     },
                        //     itemGroup: {
                        //         className: `${styles.dropdownItems}`,  // Aplica el estilo personalizado para las opciones
                        //     },
                        //     root: {
                        //         className: `${styles.dropdownItems}`
                        //     },
                        //     wrapper: {
                        //         className: `${styles.dropdownItems}`
                        //     }
                        // }}
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
                {guardarListAux && (
                  <div className="flex flex-col gap-5">
                    {guardarListAux.map((ele, index) => {
                      return (
                        <div className="flex flex-col gap-1">
                          {paymentSelected && (
                            <h2 className="text-start font-bold">
                              {ele.descripcion}
                            </h2>
                          )}

                          {ele.montoPago && (
                            <span className="flex gap-2">
                              <p>Monto a pagar:</p>
                              <p key={index}> ${ele.montoPago}</p>
                            </span>
                          )}
                          {ele.referecia != 0 && (
                            <span className="flex gap-2">
                              <p>referencia:</p>
                              <p key={index}> {ele.referecia}</p>
                            </span>
                          )}
                          {ele.periodo && (
                            <span className="flex gap-2">
                              <p>periodo:</p>
                              <p key={index}>
                                {' '}
                                {ele.periodo} {selectedPlazosList}
                              </p>
                            </span>
                          )}
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
