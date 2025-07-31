import React from 'react';
import chip from '../../../assets/chip.svg';
import mastercard from '../../../assets/mastercard.svg';
import visa from '../../../assets/visa.svg';

interface CardTemplateProps {
  nameCard: string;
  cardNumber: string;
  expiredDate: any;
}

export const CardTemplate: React.FC<CardTemplateProps> = ({
  nameCard,
  cardNumber,
  expiredDate = '',
}) => {
  const cardType = () => {
    if (cardNumber[0] == '4') return true;
    else return false;
  };

  return (
    <div
      className="relative flex h-[100%] flex-col justify-between gap-15 overflow-hidden rounded-md px-10 py-5 text-white"
      style={{
        backgroundColor: 'hsla(240,63%,67%,1)',
        backgroundImage: `
                    radial-gradient(at 99% 24%, hsla(239,82%,74%,1) 0px, transparent 50%),
                    radial-gradient(at 3% 99%, hsla(256,88%,66%,1) 0px, transparent 50%),
                    radial-gradient(at 2% 97%, hsla(298,70%,87%,1) 0px, transparent 50%),
                    radial-gradient(at 42% 92%, hsla(245,100%,51%,1) 0px, transparent 50%),
                    radial-gradient(at 86% 80%, hsla(266,100%,87%,1) 0px, transparent 50%),
                    radial-gradient(at 46% 32%, hsla(273,84%,84%,1) 0px, transparent 50%),
                    radial-gradient(at 31% 81%, hsla(146,92%,67%,1) 0px, transparent 50%),
                    radial-gradient(at 96% 52%, hsla(151,83%,65%,1) 0px, transparent 50%)
                    `,
      }}
    >
      {/* -           <div className='bg-white w-full h-10 opacity-40 absolute -left-10' ></div> */}
      {/* <div className="absolute inset-x-0 top-5 h-7 bg-white opacity-40"></div> */}

      <div className="flex justify-between">
        {/* <FcSimCardChip size={24} className='text-black'/> */}
        <img src={chip} alt="" className="h-10" />
        {cardNumber[0] == '4' ? (
          <img src={visa} alt="" className="z-20 h-7" />
        ) : (
          <img src={mastercard} alt="" className="z-20 h-10" />
        )}
      </div>
      <span>
        <p className="text-3xl font-bold">
          {cardNumber || '**** **** **** 1212'}
        </p>
      </span>
      <div className="flex justify-between">
        <span>
          <p className="text-sm">Nombre tarjeta</p>
          <p className="text-xl">{nameCard || 'Nombre apellido'}</p>
        </span>
        <span>
          <p className="text-sm">Fecha vencimiento</p>
          <p>{expiredDate || 'MM/YY'}</p>
        </span>
        <div className="absolute inset-x-90 -inset-y-40 z-10 size-80 rounded-full bg-white opacity-20"></div>
        <div className="absolute inset-x-60 -inset-y-20 z-10 size-50 rounded-full bg-white opacity-10"></div>

        <div className="absolute -inset-x-40 inset-y-30 z-10 size-100 rounded-full bg-white opacity-20"></div>
      </div>
    </div>
  );
};

// backgroundColor: 'hsla(240,63%,67%,1)',
//                 backgroundImage: `
//                     radial-gradient(at 99% 24%, hsla(239,82%,74%,1) 0px, transparent 50%),
// radial-gradient(at 3% 99%, hsla(256,88%,66%,1) 0px, transparent 50%),
// radial-gradient(at 2% 97%, hsla(298,70%,87%,1) 0px, transparent 50%),
// radial-gradient(at 42% 92%, hsla(245,100%,51%,1) 0px, transparent 50%),
// radial-gradient(at 86% 80%, hsla(266,100%,87%,1) 0px, transparent 50%),
// radial-gradient(at 46% 32%, hsla(273,84%,84%,1) 0px, transparent 50%),
// radial-gradient(at 31% 81%, hsla(146,92%,67%,1) 0px, transparent 50%),
// radial-gradient(at 96% 52%, hsla(151,83%,65%,1) 0px, transparent 50%)
