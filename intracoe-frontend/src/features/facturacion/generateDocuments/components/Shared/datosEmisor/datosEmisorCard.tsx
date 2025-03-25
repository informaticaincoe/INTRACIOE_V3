import { useEffect } from "react";
import { EmisorInterface } from "../../../../../../shared/interfaces/interfaces";
import { getAllEmpresas } from "../../../../../bussiness/configBussiness/services/empresaServices";

interface DatosEmisorData{
  emisorData: EmisorInterface,
  setEmisorData :any
}

export const DatosEmisorCard:React.FC<DatosEmisorData> = ({ emisorData, setEmisorData }) => {

  useEffect(()=>{
    fetchEmisorInfo();
  },[])

  const fetchEmisorInfo = async () => {
    try {
      const response = await getAllEmpresas();
      setEmisorData(response[0]);

    } catch (error) {
      console.log(error);
    }
  };

  return (
    <>
      <div className="grid grid-cols-[auto_1fr] items-start justify-start gap-x-10 gap-y-4 font-medium">
        <span className="text-start text-black opacity-50">NIT:</span>
        <span className="text-start">{emisorData.nit }</span>
        <span className="text-start text-black opacity-50">Nombre:</span>
        <span className="text-start">{emisorData.nombre_comercial}</span>
        <span className="text-start text-black opacity-50">Teléfono:</span>
        <span className="text-start">{emisorData.telefono}</span>
        <span className="text-start text-black opacity-50">Correo:</span>
        <span className="text-start">{emisorData.email}</span>
        <span className="text-start text-black opacity-50">
          Dirección comercial:
        </span>
        <span className="text-start">{emisorData.direccion_comercial}</span>
      </div>
    </>
  );
};
