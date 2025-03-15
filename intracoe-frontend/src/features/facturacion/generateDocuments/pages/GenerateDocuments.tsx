import { Divider } from "primereact/divider";
import { WhiteSectionsPage } from "../../../../shared/containers/whiteSectionsPage";
import { Title } from "../../../../shared/text/title";

export const GenerateDocuments = () => {
  return (
    <>
      <Title text="Generar documentos" />

      <WhiteSectionsPage>
        <>
          <h1 className="font-bold text-start">Datos del emisor</h1>
          <Divider className="m-0 p-0"></Divider>
          <table>
            
          </table>

          <span>
            <span className="flex gap-5">
              <p className="text-black opacity-70">NIT:</p>
              <p>123456789</p>
            </span>
            <span className="flex gap-5">
              <p className="text-black opacity-70">Nombre:</p>
              <p>inversiones Comerciales Escobar</p>
            </span>
            <span className="flex gap-5">
              <p className="text-black opacity-70">Teléfono:</p>
              <p>123456789</p>
            </span>
            <span className="flex gap-5">
              <p className="text-black opacity-70">Dirección comercial:</p>
              <p>123456789</p>
            </span>
          </span>
        </>
      </WhiteSectionsPage>

    </>
  );
};
