import { Divider } from 'primereact/divider';
import { WhiteSectionsPage } from '../../../../shared/containers/whiteSectionsPage';
import { Title } from '../../../../shared/text/title';
import { useEffect, useState } from 'react';
import { getAllEmpresas } from '../../../bussiness/configBussiness/services/empresaServices';
import { DatosEmisorCard } from '../components/datosEmisorCard';
import { DropDownTipoDte } from '../components/configuracionFactura/DropdownTipoDte';
import { SelectCondicionOperacion } from '../components/configuracionFactura/selectCondicionOperacion';
import { SelectModeloFactura } from '../components/configuracionFactura/selectModeloFactura';
import { SelectTipoTransmisión } from '../components/configuracionFactura/selectTipoTransmisión';
import { CheckBoxVentaTerceros } from '../components/configuracionFactura/checkboxVentaTerceros';
import { IdentifcacionSeccion } from '../components/identificacion.tsx/identifcacionSeccion';
import { SelectReceptor } from '../components/receptor/SelectReceptor';
import { TablaProductosAgregados } from '../components/productosAgregados/tablaProductosAgregados';
import { ModalListaProdcutos } from '../components/productosAgregados/modalListaProdcutos';
import { FormasdePago } from '../components/configuracionFactura/formasdePago';

export const GenerateDocuments = () => {
  const [emisorData, setEmisorData] = useState({
    nit: '',
    nombre: '',
    telefono: '',
    email: '',
    direccion_comercial: '',
  });
  const [showProductsModal, setShowProductsModal] = useState(false);

  useEffect(() => {
    fetchEmisarInfo();
  }, []);

  const fetchEmisarInfo = async () => {
    try {
      const response = await getAllEmpresas();
      setEmisorData({
        nit: response[0].nit,
        nombre: response[0].nombre_razon_social,
        telefono: response[0].telefono,
        email: response[0].email,
        direccion_comercial: response[0].direccion_comercial,
      });
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <>
      <Title text="Generar documentos" />

      <DatosEmisorCard
        nit={emisorData.nit}
        nombre={emisorData.nombre}
        telefono={emisorData.telefono}
        email={emisorData.email}
        direccion_comercial={emisorData.direccion_comercial}
      />

      {/*Seccion configuración de factura*/}
      <WhiteSectionsPage>
        <>
          <div className="pt2 pb-5">
            <h1 className="text-start text-xl font-bold">
              Configuración factura
            </h1>
            <Divider className="m-0 p-0"></Divider>
            <div className="flex flex-col gap-8">
              <DropDownTipoDte />
              <SelectCondicionOperacion />
              <SelectModeloFactura />
              <SelectTipoTransmisión />
              <FormasdePago />
              <CheckBoxVentaTerceros />
            </div>
          </div>
        </>
      </WhiteSectionsPage>

      {/*Seccion identificación*/}
      <WhiteSectionsPage>
        <div className="pt2 pb-5">
          <h1 className="text-start text-xl font-bold">Identificación</h1>
          <Divider className="m-0 p-0"></Divider>
          <IdentifcacionSeccion />
        </div>
      </WhiteSectionsPage>

      {/*Seccion receptor*/}
      <WhiteSectionsPage>
        <div className="pt2 pb-5">
          <h1 className="text-start text-xl font-bold">
            Seleccione el receptor
          </h1>
          <Divider className="m-0 p-0"></Divider>
          <SelectReceptor />
        </div>
      </WhiteSectionsPage>

      {/*Seccion productos*/}
      <WhiteSectionsPage>
        <div className="pt-2 pb-5">
          <div className="flex justify-between">
            <h1 className="text-start text-xl font-bold">
              Productos agregados
            </h1>
            <button
              className="bg-primary-blue rounded-md px-5 py-3 text-white hover:cursor-pointer"
              onClick={() => setShowProductsModal(true)}
            >
              Añadir producto
            </button>
          </div>
          <Divider className="m-0 p-0"></Divider>
          <TablaProductosAgregados />
          <ModalListaProdcutos
            visible={showProductsModal}
            setVisible={setShowProductsModal}
          />
        </div>
      </WhiteSectionsPage>
    </>
  );
};
