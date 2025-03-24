import { Divider } from 'primereact/divider';
import { WhiteSectionsPage } from '../../../../shared/containers/whiteSectionsPage';
import { Title } from '../../../../shared/text/title';
import { useEffect, useState } from 'react';
import { DatosEmisorCard } from '../components/Shared/datosEmisor/datosEmisorCard';
import { DropDownTipoDte } from '../components/Shared/configuracionFactura/tipoDocumento/DropdownTipoDte';
import { SelectCondicionOperacion } from '../components/Shared/configuracionFactura/condicionOperacion/selectCondicionOperacion';
import { SelectTipoTransmisión } from '../components/Shared/configuracionFactura/tipoTransmision/selectTipoTransmisión';
import { CheckBoxVentaTerceros } from '../components/Shared/configuracionFactura/ventaTerceros/checkboxVentaTerceros';
import { IdentifcacionSeccion } from '../components/Shared/identificacion.tsx/identifcacionSeccion';
import { SelectReceptor } from '../components/Shared/receptor/SelectReceptor';
import { TablaProductosAgregados } from '../components/FE/productosAgregados/tablaProductosAgregados';
import { ModalListaProdcutos } from '../components/FE/productosAgregados/modalListaProdcutos';
import { FormasdePagoForm } from '../components/Shared/configuracionFactura/formasDePago/formasdePagoForm';
import { ModalListaFacturas } from '../components/Shared/tablaFacturasSeleccionar/modalListaFacturas';
import { TablaProductosFacturaNotasCredito } from '../components/NotaCredito/tablaProductosFacturaNotasCredito';
import { TablaProductosFacturaNotasDebito } from '../components/NotaDebito/TablaProductosFacturaNotasDebito';
import { TablaProductosCreditoFiscal } from '../components/CreditoFiscal/TablaProductosCreditoFiscal';
import { ButtonDocumentosRelacionados } from '../components/Shared/configuracionFactura/documentosRelacionados/ButtonDocumentosRelacionados';
import { SelectModeloFactura } from '../components/Shared/configuracionFactura/modeloDeFacturacion/selectModeloFactura';
import { SendFormButton } from '../../../../shared/buttons/sendFormButton';
import { defaulReceptorData, ReceptorInterface } from '../../../../shared/interfaces/interfaces';
import { ProductosTabla } from '../components/FE/productosAgregados/productosData';
import { ResumenTotalesCard } from '../components/Shared/resumenTotales/resumenTotalesCard';

export const GenerateDocuments = () => {
  const [showProductsModal, setShowProductsModal] = useState(false);
  const [showfacturasModal, setShowfacturasModal] = useState(false);
  const [visibleDocumentoRelacionadomodal, setVisibleDocumentoRelacionadomodal] = useState(false);
  const [condicionDeOperacion, setCondicionDeOperacion] = useState<string>("01") //Id de la condicion de operacion
  const [receptor, setReceptor] = useState<ReceptorInterface>(defaulReceptorData)
  const [tipoDocumento, setTipoDocumento] = useState<{
    name: string;
    code: string;
  }>();
  const [listProducts, setListProducts] = useState<ProductosTabla[]>([])

  let SubTotal = 0

  const generarFactura = () => {
    const data = {
      "tipo_documento_seleccionado": tipoDocumento?.code,
      "tipooperacion_id": condicionDeOperacion,
      "tipomodelo_obj": condicionDeOperacion,
      "recptor_temp": receptor //TODO: obtener toda la informacion por medio del id
    }
    console.log(data)
  }
  //************************************/
  // OBTENCION DE DATOS
  //************************************/
  useEffect(() => {
    console.log("list:", listProducts);
  }, [listProducts]);

  // useEffect(() => {
  //   console.log("condicionDeOperacion:", condicionDeOperacion);
  // }, [condicionDeOperacion]);

  // useEffect(() => {
  //   console.log('tipoDocumento', tipoDocumento);
  // }, [tipoDocumento]);

  //************************************/
  // CONSUMO DE API
  //************************************/

  {/*******************************/ }


  return (
    <>
      <Title text="Generar documentos" />

      {/* Seccion datos del emisor */}
      <WhiteSectionsPage>
        <>
          <div className="pt2 pb-5">
            <h1 className="text-start text-xl font-bold">Datos del emisor</h1>
            <Divider className="m-0 p-0"></Divider>
            <DatosEmisorCard />
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
              <div className="flex flex-col items-start gap-1">
                <label className="opacity-70">Tipo de documento</label>
                <DropDownTipoDte
                  tipoDocumento={tipoDocumento}
                  setTipoDocumento={setTipoDocumento}
                />
              </div>
              <SelectCondicionOperacion condicionDeOperacion={condicionDeOperacion} setCondicionDeOperacion={setCondicionDeOperacion} />
              <SelectModeloFactura />
              <SelectTipoTransmisión />
              {tipoDocumento?.code != "04" && <FormasdePagoForm />}
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
          <SelectReceptor receptor={receptor} setReceptor={setReceptor} />
        </div>
      </WhiteSectionsPage>

      {/********* Seccion productos *********/}
      {/* Tipo de documento: FE */}
      {tipoDocumento?.code === "01" && (
        <WhiteSectionsPage>
          <div className="pt-2 pb-5">
            <div className="flex justify-between">
              <h1 className="text-start text-xl font-bold">
                Productos agregados
              </h1>
              <span className='flex gap-4'>
                <ButtonDocumentosRelacionados visible={visibleDocumentoRelacionadomodal} setVisible={setVisibleDocumentoRelacionadomodal} />
                <SendFormButton
                  className="bg-primary-blue rounded-md px-5 text-white hover:cursor-pointer text-nowrap"
                  onClick={() => setShowProductsModal(true)}
                  text={"Añadir producto"}
                />
              </span>
            </div>

            <Divider className=""></Divider>
            <TablaProductosAgregados listProducts={listProducts} setListProducts={setListProducts} />
            <ModalListaProdcutos
              visible={showProductsModal}
              setVisible={setShowProductsModal}
              setListProducts={setListProducts}
            />
          </div>
        </WhiteSectionsPage>
      )}

      {/* Tipo de documento: Nota de Creditos */}
      {tipoDocumento?.code === "04" && (
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
      {tipoDocumento?.code === "05" && (
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
      {tipoDocumento?.code === "02" && (
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
              setListProducts={setListProducts}
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
          <ResumenTotalesCard listProducts={listProducts}/>
        </div>
      </WhiteSectionsPage>

      <div className="mx-14 flex">
        <button
          type="button"
          className="bg-primary-yellow mb-5 self-start rounded-md px-5 py-3 text-white hover:cursor-pointer"
          onClick={() => generarFactura()}
        >
          Generar factura
        </button>
      </div>
    </>
  );
};
