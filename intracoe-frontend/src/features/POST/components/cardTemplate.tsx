import React from 'react'
import { FaCcMastercard } from 'react-icons/fa6'
import { LuWifi } from 'react-icons/lu'

interface CardTemplateProps {
    nameCard: string,
    cardNumber: string,
    expiredDateMonth: string,
    expiredDateYear: string
}

export const CardTemplate: React.FC<CardTemplateProps> = ({ nameCard, cardNumber, expiredDateMonth, expiredDateYear }) => {
    return (
        <div
            className='relative text-white rounded-md px-10 py-5 h-60 flex flex-col justify-between'
            style={{
                backgroundColor: 'hsla(263,96%,59%,1)',
                backgroundImage: `
                    radial-gradient(at 19% 61%, hsla(209,65%,73%,1) 0px, transparent 50%),
                    radial-gradient(at 49% 47%, hsla(278,95%,75%,1) 0px, transparent 50%),
                    radial-gradient(at 6% 12%, hsla(298,99%,66%,1) 0px, transparent 50%),
                    radial-gradient(at 26% 16%, hsla(28,60%,78%,1) 0px, transparent 50%),
                    radial-gradient(at 86% 90%, hsla(286,95%,84%,1) 0px, transparent 50%)`
            }}>
            {/* -           <div className='bg-white w-full h-10 opacity-40 absolute -left-10' ></div> */}
            {/* <div className="absolute inset-x-0 top-5 h-7 bg-white opacity-40"></div> */}


            <div className='flex justify-between'>
                <h1 className='font-bold font-5xl'>Datos tarjeta</h1>
            </div>
            <div className='flex justify-between'>
                <span>
                    <p>{nameCard || "Nombre Apellidos"}</p>
                    <p className='text-2xl font-bold'>{cardNumber || "1234 5678 9101 1212"}</p>
                </span>
                <span>
                    <p>{expiredDateMonth || "04"}/{expiredDateYear || "25"}</p>
                    <FaCcMastercard size={35} className='opacity-70' />
                </span>
            </div>
        </div>
    )
}
