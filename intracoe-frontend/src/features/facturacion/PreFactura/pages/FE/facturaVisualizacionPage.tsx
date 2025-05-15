import { useParams } from "react-router";
import { FacturaConsumirdorFinalPage } from "./facturaConsumidorFinalPage";
import { SujetoExcluidoPage } from "./sujetoExcluidoPage";
import { useEffect } from "react";

export const FacturaVisualizacionPage = () => {
  const { id, codigo } = useParams();

  useEffect(() => {
    console.log({ id, codigo });
  }, []);

  if (id && (codigo === '01' || codigo === '03')) {
    return <FacturaConsumirdorFinalPage id={id} />;
  }

  if (id && codigo === '14') {
    return <SujetoExcluidoPage id={id} />;
  }

  return <div>Tipo de factura no reconocido</div>;
};
