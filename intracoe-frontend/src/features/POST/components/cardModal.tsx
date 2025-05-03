import { Dialog } from 'primereact/dialog';
import React, { useState } from 'react'
import { CardTemplate } from './cardTemplate';
import { IconField } from "primereact/iconfield";
import { InputIcon } from "primereact/inputicon";
import { InputText } from "primereact/inputtext";
import { IoPersonOutline } from 'react-icons/io5';
import mastercard from "../../../assets/mastercardIcon.svg"
import visa from "../../../assets/visa.svg"

import password from "../../../assets/password.svg"
import { Calendar } from 'primereact/calendar';
import { InputMask } from "primereact/inputmask";
import { Password } from 'primereact/password';
import { CiCalendar } from 'react-icons/ci';
import dayjs from 'dayjs';


interface CardModalProps {
    visible: boolean,
    setVisible: any
}

export const CardModal: React.FC<CardModalProps> = ({ visible, setVisible }) => {

    const [formData, setFormData] = useState({
        cardName: "",
        cardNumber: "",
        expiredDate: undefined,
        CVV: ""
    })

    const handleChangeForm = (e: any) => {
        const { name, value } = e.target;

        // Si el campo es la fecha de vencimiento, formateamos la fecha a 'MM/YY' usando dayjs
        if (name === 'expiredDate' && value) {
            const formattedDate = dayjs(value).format('MM/YY'); // Formateamos la fecha a 'MM/YY'
            setFormData({ ...formData, [name]: formattedDate });
        } else {
            setFormData({ ...formData, [name]: value });
        }
    }

    const handlerForm = (e: React.FormEvent) => {
        e.preventDefault();


    }
    return (
        <Dialog header={<p>POST</p>} visible={visible} onHide={() => { if (!visible) return; setVisible(false); }}
            style={{ width: '35vw' }} breakpoints={{ '1679': '30vw', '1462px': '45vw', }}>

            <div className='px-8'>
                <CardTemplate nameCard={formData.cardName} cardNumber={formData.cardNumber} expiredDate={formData.expiredDate}></CardTemplate>

                <form action="" className='flex flex-col gap-5 py-10'>
                    <span>
                        <label htmlFor="cardName" className='opacity-70'>Nombre tarjeta</label>
                        <IconField iconPosition="left">
                            <InputIcon> <IoPersonOutline /></InputIcon>
                            <InputText placeholder="Nombre apellido" style={{ width: '100%', paddingLeft: '3rem' }} name="cardName" onChange={(e: any) => handleChangeForm(e)} />
                        </IconField>
                    </span>
                    <div className='flex gap-5'>
                        <span className='flex flex-col w-full'>
                            <label htmlFor="cardNumber" className='opacity-70'>Numero tarjeta</label>
                            <IconField iconPosition="left">
                                <InputIcon>
                                    {
                                        (formData.cardNumber[0] == '4') ?
                                            <embed src={visa} className='w-7' />
                                            :
                                            <embed src={mastercard} className='h-3' />
                                    }

                                </InputIcon>
                                <InputMask mask="9999 9999 9999 9999" placeholder="0000 0000 0000 0000" style={{ width: '100%', padding:'2% 8%' }} name="cardNumber" value={formData.cardNumber} onChange={(e) => handleChangeForm(e)}></InputMask>
                            </IconField>
                        </span>
                    </div>
                    <div className='flex gap-5'>
                        <span>
                            <label htmlFor="expiredDate" className='opacity-70'>Fecha vencimiento</label>

                            <Calendar
                                name="expiredDate"
                                value={formData.expiredDate ? dayjs(formData.expiredDate, 'MM/YY').toDate() : null} // Convertimos la fecha en formato MM/YY
                                onChange={handleChangeForm}
                                dateFormat="mm/yy"
                                view='month'
                                showIcon
                                icon={<CiCalendar size={20} color='rgba(0,0,0,0.5)' />}
                                iconPos="left"

                            />
                        </span>
                        <span>
                            <label htmlFor="CVV" className='opacity-70'>CVV</label>
                            <IconField iconPosition="left">
                                <InputIcon>
                                    <embed src={password} className='h-5 flex items-center opacity-60' />

                                </InputIcon>
                                <Password
                                    name="CVV"
                                    value={formData.CVV}
                                    panelStyle={{ display: 'none' }}
                                    onChange={(e: any) => handleChangeForm(e)}
                                    toggleMask
                                />
                            </IconField>
                        </span>

                    </div>
                </form>
            </div>
        </Dialog>


    )
}
