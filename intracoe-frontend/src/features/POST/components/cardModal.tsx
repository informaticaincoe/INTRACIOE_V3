import { Dialog } from 'primereact/dialog';
import React, { useState } from 'react'
import { CardTemplate } from './cardTemplate';
import { Input } from '../../../shared/forms/input';
import { FaCcMastercard } from "react-icons/fa6";

interface CardModalProps {
    visible: boolean,
    setVisible: any
}

export const CardModal: React.FC<CardModalProps> = ({ visible, setVisible }) => {

    const [formData, setFormData] = useState({
        cardName: "",
        cardNumber: "",
        expiredDateMonth: "",
        expiredDateYear: "",
        CVV: ""
    })

    const handleChangeForm = (e: any) => {
        setFormData({ ...formData, [e.target.name]: [e.target.value] })
    }

    const handlerForm = (e: React.FormEvent) => {
        e.preventDefault();
    }
    return (
        <Dialog header={<p>POST</p>} visible={visible} onHide={() => { if (!visible) return; setVisible(false); }}
            style={{ width: '40vw' }} breakpoints={{ '960px': '75vw', '641px': '100vw' }}>

            <div>
                <CardTemplate nameCard={formData.cardName} cardNumber={formData.cardNumber} expiredDateMonth={formData.expiredDateMonth} expiredDateYear={formData.expiredDateYear}></CardTemplate>

                <form action="" className='flex flex-col gap-5 py-10'>
                    <span>
                        <label htmlFor="cardName" className='opacity-70'>Nombre tarjeta</label>
                        <Input name="cardName" value={formData.cardName} onChange={(e: any) => handleChangeForm(e)} />
                    </span>
                    <div className='flex'>
                        <span  className='flex flex-col w-full'>
                            <label htmlFor="cardNumber" className='opacity-70'>Numero tarjeta</label>
                            <Input name="cardNumber" value={formData.cardNumber} onChange={(e: any) => handleChangeForm(e)} className='w-full' />
                        </span>
                        
                    </div>
                    <div className='flex gap-5'>
                        <span>
                            <label htmlFor="expiredDateMonth" className='opacity-70'>Mes</label>
                            <Input name="expiredDateMonth" value={formData.expiredDateMonth} onChange={(e: any) => handleChangeForm(e)} />
                        </span><span>
                            <label htmlFor="expiredDateYear" className='opacity-70'>Año</label>
                            <Input name="expiredDateYear" value={formData.expiredDateYear} onChange={(e: any) => handleChangeForm(e)} />
                        </span>
                        <span>
                            <label htmlFor="CVV" className='opacity-70'>CVV</label>
                            <Input type='password' name="CVV" value={formData.CVV} onChange={(e: any) => handleChangeForm(e)} />
                        </span>
                    </div>
                </form>
            </div>
        </Dialog>


    )
}
