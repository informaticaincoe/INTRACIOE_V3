const Data = {
  numeroControl: 'DTE-01-0000MOO1-000000000000100',
  CodigoGeneracion: '2B51B3C4-33FE-43A9-BBDA-4648ADDD0BAF',
};

interface IdentifcacionSeccionProps {
  tipoDocumento:string,
  tipoEstablecimiento:string,
  puntoVenta:string
}

export const IdentifcacionSeccion:React.FC<IdentifcacionSeccionProps> = ({ tipoDocumento, tipoEstablecimiento, puntoVenta }) => {
  var dateVariable = new Date();
  var numeroDeContro = 0

  const GenerarNumeroDeControl = () => {
    return 'DTE-' + tipoDocumento + '00' + tipoEstablecimiento + puntoVenta
  }
  return (
    <>
      <div className="grid grid-cols-[auto_1fr] items-start justify-start gap-4 font-medium">
        <span className="text-start text-black opacity-50">
          Número de control:
        </span>
        <span className="text-start">{GenerarNumeroDeControl()}</span>
        <span className="text-start text-black opacity-50">
          Codigo de generación:
        </span>
        <span className="text-start">{Data.CodigoGeneracion}</span>
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
