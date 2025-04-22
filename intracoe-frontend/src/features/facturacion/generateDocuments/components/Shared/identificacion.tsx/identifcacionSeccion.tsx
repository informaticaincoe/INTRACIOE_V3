import { useEffect } from 'react';

interface IdentifcacionSeccionProps {
  codigoGeneracion: string;
  numeroControl: string;
}

export const IdentifcacionSeccion: React.FC<IdentifcacionSeccionProps> = ({
  codigoGeneracion,
  numeroControl,
}) => {
  var dateVariable = new Date();

  return (
    <>
      <div className="grid grid-cols-[auto_1fr] items-start justify-start gap-4 font-medium">
        <span className="text-start text-black opacity-50">
          Número de control:
        </span>
        <span className="text-start">{numeroControl}</span>
        <span className="text-start text-black opacity-50">
          Codigo de generación:
        </span>
        <span className="text-start">{codigoGeneracion}</span>
        <span className="text-start text-black opacity-50">
          Fecha de generación:
        </span>
        <span className="text-start">
          {dateVariable.getDay() +
            '/' +
            dateVariable.getMonth() +
            '/' +
            dateVariable.getFullYear()}
        </span>
        <span className="text-start text-black opacity-50">
          Hora de generación:
        </span>
        <span className="text-start">
          {dateVariable.getHours() +
            ':' +
            dateVariable.getMinutes() +
            ':' +
            dateVariable.getSeconds()}
        </span>
      </div>
    </>
  );
};
