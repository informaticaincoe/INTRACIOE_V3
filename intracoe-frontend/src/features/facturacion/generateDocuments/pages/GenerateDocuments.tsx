import { Divider } from 'primereact/divider';
import { WhiteSectionsPage } from '../../../../shared/containers/whiteSectionsPage';
import { Title } from '../../../../shared/text/title';
import { useEffect, useState } from 'react';
import { getAllEmpresas } from '../../../bussiness/configBussiness/services/empresaServices';
import { DatosEmisorCard } from '../components/Shared/datosEmisor/datosEmisorCard';
import { DropDownTipoDte } from '../components/Shared/configuracionFactura/DropdownTipoDte';
import { SelectCondicionOperacion } from '../components/Shared/configuracionFactura/selectCondicionOperacion';
import { SelectModeloFactura } from '../components/Shared/configuracionFactura/selectModeloFactura';
import { SelectTipoTransmisión } from '../components/Shared/configuracionFactura/selectTipoTransmisión';
import { CheckBoxVentaTerceros } from '../components/Shared/configuracionFactura/checkboxVentaTerceros';
import { IdentifcacionSeccion } from '../components/Shared/identificacion.tsx/identifcacionSeccion';
import { SelectReceptor } from '../components/Shared/receptor/SelectReceptor';
import { TablaProductosAgregados } from '../components/FE/productosAgregados/tablaProductosAgregados';
import { ModalListaProdcutos } from '../components/FE/productosAgregados/modalListaProdcutos';
import { FormasdePago } from '../components/Shared/configuracionFactura/formasdePago';
import { ModalListaFacturas } from '../components/Shared/tablaFacturas/modalListaFacturas';
import { TablaProductosFacturaNotasCredito } from '../components/NotaCredito/tablaProductosFacturaNotasCredito';
import { TablaProductosFacturaNotasDebito } from '../components/NotaDebito/TablaProductosFacturaNotasDebito';
import { TablaProductosCreditoFiscal } from '../components/CreditoFiscal/TablaProductosCreditoFiscal';

export const GenerateDocuments = () => {
  const [emisorData, setEmisorData] = useState({
    nit: '',
    nombre: '',
    telefono: '',
    email: '',
    direccion_comercial: '',
  });
  const [showProductsModal, setShowProductsModal] = useState(false);
  const [showfacturasModal, setShowfacturasModal] = useState(false);

  const [tipoDocumento, setTipoDocumento] = useState<{
    name: string;
    code: number;
  }>();

  useEffect(() => {
    fetchEmisarInfo();
  }, []);

  useEffect(() => {
    console.log('tipoDocumento', tipoDocumento);
  }, [tipoDocumento]);

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

  const generarFactura = () => {
    console.log('enviado');
  };
  return (
    <>
      <Title text="Generar documentos" />

      {/* Seccion datos del emisor */}
      <WhiteSectionsPage>
        <>
          <div className="pt2 pb-5">
            <h1 className="text-start text-xl font-bold">Datos del emisor</h1>
            <Divider className="m-0 p-0"></Divider>
            <DatosEmisorCard
              nit={emisorData.nit}
              nombre={emisorData.nombre}
              telefono={emisorData.telefono}
              email={emisorData.email}
              direccion_comercial={emisorData.direccion_comercial}
            />
          </div>
        </>
      </WhiteSectionsPage>

      {/*Seccion configuración de factura*/}
      <WhiteSectionsPage>
        <>
          <div className="pt2 pb-5">
            <h1 className="text-start text-xl font-bold">
              Configuración factura
            </h1>
            <Divider className="m-0 p-0"></Divider>
            <div className="flex flex-col gap-8">
              <DropDownTipoDte
                tipoDocumento={tipoDocumento}
                setTipoDocumento={setTipoDocumento}
              />
              <SelectCondicionOperacion />
              <SelectModeloFactura />
              <SelectTipoTransmisión />
              {
                tipoDocumento?.code != 4 &&
                <FormasdePago />
              }
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
      {/* Tipo de documento: FE */}
      {tipoDocumento?.code === 1 && (
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
      )}

      {/* Tipo de documento: Nota de Creditos */}
      {tipoDocumento?.code === 4 && (
        <WhiteSectionsPage>
          <div className="pt-2 pb-5">
            <div className="flex justify-between">
              <h1 className="text-start text-xl font-bold">
                Factura seleccionada
              </h1>
              <button
                className="bg-primary-blue rounded-md px-5 py-3 text-white hover:cursor-pointer"
                onClick={() => setShowfacturasModal(true)}
              >
                seleccionar factura
              </button>
            </div>
            <Divider className="m-0 p-0"></Divider>
            <TablaProductosFacturaNotasCredito />
            <ModalListaFacturas
              visible={showfacturasModal}
              setVisible={setShowfacturasModal}
            />
          </div>
        </WhiteSectionsPage>
      )}

      {/* Tipo de documento: Nota de Debito */}
      {tipoDocumento?.code === 5 && (
        <WhiteSectionsPage>
          <div className="pt-2 pb-5">
            <div className="flex justify-between">
              <h1 className="text-start text-xl font-bold">
                Factura seleccionada
              </h1>
              <button
                className="bg-primary-blue rounded-md px-5 py-3 text-white hover:cursor-pointer"
                onClick={() => setShowfacturasModal(true)}
              >
                seleccionar factura
              </button>
            </div>
            <Divider className="m-0 p-0"></Divider>
            <TablaProductosFacturaNotasDebito />
            <ModalListaFacturas
              visible={showfacturasModal}
              setVisible={setShowfacturasModal}
            />
          </div>
        </WhiteSectionsPage>
      )}

      {/* Tipo de documento: Credito fiscal */}
      {tipoDocumento?.code === 2 && (
        <WhiteSectionsPage>
          <div className="pt-2 pb-5">
            <div className="flex justify-between">
              <h1 className="text-start text-xl font-bold">
                Factura seleccionada
              </h1>
              <button
                className="bg-primary-blue rounded-md px-5 py-3 text-white hover:cursor-pointer"
                onClick={() => setShowProductsModal(true)}
              >
                Seleccionar productos
              </button>
            </div>
            <Divider className="m-0 p-0"></Divider>
            <TablaProductosCreditoFiscal />
            <ModalListaProdcutos
              visible={showProductsModal}
              setVisible={setShowProductsModal}
            />
          </div>
        </WhiteSectionsPage>
      )}

      {/*Seccion totales resumen*/}
      <WhiteSectionsPage>
        <div className="pt-2 pb-5">
          <div className="flex justify-between">
            <h1 className="text-start text-xl font-bold">Resumen de totales</h1>
          </div>
          <Divider className="m-0 p-0"></Divider>
          <div className="grid grid-cols-4 gap-4 text-start">
            <p className="opacity-60">SubTotal Neto:</p>
            <p>$21.24</p>

            <p className="opacity-60">Total IVA:</p>
            <p>$2.78</p>

            <p className="opacity-60">Total con IVA:</p>
            <p>$21.24</p>

            <p className="opacity-60">Monto descuento:</p>
            <p>$0.0</p>

            <p>Total a pagar:</p>
            <p>$21.60</p>
          </div>
        </div>
      </WhiteSectionsPage>

      <div className="mx-14 flex">
        <button
          type="button"
          className="bg-primary-yellow mb-5 self-start rounded-md px-5 py-3 text-white hover:cursor-pointer"
          onClick={generarFactura}
        >
          Generar factura
        </button>
      </div>
    </>
  );
};
