import { useEffect, useState } from 'react'
import { PaymentMethodInteface, paymentMethodsList } from './formasdePagoData'
import { Dropdown } from 'primereact/dropdown';
import { FaRegCreditCard } from "react-icons/fa6";
import { MultiSelect, MultiSelectChangeEvent } from 'primereact/multiselect';
import { Input } from '../../../../../shared/forms/input';
import { InputNumber } from 'primereact/inputnumber';


export const FormasdePago = () => {
    const [listFormasdePago, setListFormasdePago] = useState<PaymentMethodInteface[]>([]);
    const [paymentSelected, setPaymentSelected] = useState<PaymentMethodInteface[]>([]);

    const [formData, setFormData] = useState({
        montoPago: 0,
        referecia: 0,
        periodo: '',
    });

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    useEffect(() => {
        fetchActividadesList();
    }, []);

    const fetchActividadesList = () => {
        setListFormasdePago(paymentMethodsList)
    };


    return (
        <div className='flex flex-col w-full items-start'>
            <p className='opacity-70 text-start'>Métodos de pago</p>
            <div className="py-5">
                <ul className='grid grid-cols-3 gap-5 '>

                    <div>
                        <h2
                            className="text-black text-start font-semibold"
                        >
                            <div>
                                <Dropdown
                                    value={paymentSelected}
                                    onChange={(e: MultiSelectChangeEvent) => setPaymentSelected(e.value)}
                                    options={listFormasdePago}
                                    optionLabel="descripcion"
                                    placeholder="Seleccionar actividad economica"
                                    className={`w-full text-start mb-5`}
                                    filter
                                />
                            </div>
                        </h2>
                        <div className='flex flex-col gap-3 border border-gray-200 px-10 py-8 rounded-md'>
                            <span className='flex flex-col'>
                                <label htmlFor="montoPagar" className='text-start opacity-70'>Monto a pagar</label>
                                <div className="p-inputgroup flex-1">
                                    <span className="p-inputgroup-addon">$</span>
                                    <InputNumber placeholder="Price" />
                                </div>
                            </span>
                            <span className='flex flex-col'>
                                <label htmlFor="referencia" className='text-start opacity-70'>Referencia</label>
                                <div className="p-inputgroup flex-1">
                                    <span className="p-inputgroup-addon"><FaRegCreditCard /></span>
                                    <InputNumber placeholder="Price" />
                                </div>
                            </span>
                            <span className='flex flex-col pb-5'>
                                <label htmlFor="periodo" className='text-start opacity-70'>Periodo</label>
                                <Input
                                    name="periodo"
                                    placeholder="periodo"
                                    type="text"
                                    value={formData.periodo}
                                    onChange={handleChange}
                                />
                            </span>
                            <span className='flex justify-between gap-5'>
                                <button className='border border-primary-blue text-primary-blue rounded-md py-2 w-full'>Limpiar</button>
                                <button className='bg-primary-blue text-white rounded-md py-2 w-full'>Añadir</button>
                            </span>
                        </div>
                    </div>
                </ul>
            </div>
        </div>
    )
}
