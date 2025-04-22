import { EmisorInterface } from '../../../../../../shared/interfaces/interfaces';

interface DatosEmisorData {
  emisorData: EmisorInterface;
}

export const DatosEmisorCard: React.FC<DatosEmisorData> = ({ emisorData }) => {
  return (
    <>
      {emisorData && emisorData.nit && (
        <div className="grid grid-cols-[auto_1fr] items-start justify-start gap-x-10 gap-y-4 font-medium">
          <span className="text-start text-black opacity-50">NIT:</span>
          <span className="text-start">{emisorData.nit}</span>
          <span className="text-start text-black opacity-50">Nombre:</span>
          <span className="text-start">{emisorData.nombre_razon_social}</span>
          <span className="text-start text-black opacity-50">Teléfono:</span>
          <span className="text-start">{emisorData.telefono}</span>
          <span className="text-start text-black opacity-50">Correo:</span>
          <span className="text-start">{emisorData.email}</span>
          <span className="text-start text-black opacity-50">
            Dirección comercial:
          </span>
          <span className="text-start">{emisorData.direccion_comercial}</span>
        </div>
      )}
    </>
  );
};
