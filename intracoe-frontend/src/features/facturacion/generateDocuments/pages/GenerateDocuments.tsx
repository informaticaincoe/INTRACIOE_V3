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
import { defaulReceptorData, defaultEmisorData, EmisorInterface, ReceptorInterface } from '../../../../shared/interfaces/interfaces';
import { ProductosTabla } from '../components/FE/productosAgregados/productosData';
import { ResumenTotalesCard } from '../components/Shared/resumenTotales/resumenTotalesCard';
import { generarFacturaService, getFacturaCodigos } from '../services/factura/facturaServices';
import { CheckBoxRetencion } from '../components/Shared/configuracionFactura/Retencion/checkBoxRetencion';
import { InputTextarea } from 'primereact/inputtextarea';
import { useNavigate } from 'react-router';

export const GenerateDocuments = () => {
  const [showProductsModal, setShowProductsModal] = useState(false);
  const [showfacturasModal, setShowfacturasModal] = useState(false);
  const [visibleDocumentoRelacionadomodal, setVisibleDocumentoRelacionadomodal] = useState(false);
  const [condicionDeOperacion, setCondicionDeOperacion] = useState<string>("01") //Id de la condicion de operacion
  const [receptor, setReceptor] = useState<ReceptorInterface>(defaulReceptorData)
  const [emisorData, setEmisorData] = useState<EmisorInterface>(defaultEmisorData);
  const [tipoDocumento, setTipoDocumento] = useState<{ name: string; code: string; }>({ name: "Factura", code: "01" });
  const [listProducts, setListProducts] = useState<ProductosTabla[]>([])
  const [idListProducts, setIdListProducts] = useState<string[]>([])
  const [cantidadListProducts, setCantidadListProducts] = useState<string[]>([])
  const [formasPagoList, setFormasPagoList] = useState<any[]>([])
  const [numeroControl, setNumeroControl] = useState("");
  const [codigoGeneracion, setCodigoGeneracion] = useState("");
  const [observaciones, setObservaciones] = useState<string>("");
  const [retencionIva, setRetencionIva] = useState<number>(0)
  const [tieneRetencionIva, setTieneRetencionIva] = useState<boolean>(false)
  const [descuentoGeneral, setDescuentoGeneral] = useState<number>(0)
  const [descuentoItem, setDescuentoItem] = useState<number>(0)

  const navigate = useNavigate()

  const generarFactura = async () => {
    
    const data = {
      /*Datos del receptor*/
      "codigo_generacion": codigoGeneracion,
      "numero_control": numeroControl,
      "receptor_id": receptor.id,
      "nit_receptor": receptor.num_documento,
      "nombre_receptor": receptor.nombre,
      "direccion_receptor": receptor.direccion,
      "telefono_receptor": receptor.telefono,
      "correo_receptor": receptor.correo,
      "tipo_item_select": 1, //TODO: obtener segun la lista de productos de forma dinamica
      /*documentos relacionados*/
      "documento_seleccionado": "", //TODO: documentos relacionados
      "documento_select": "",//TODO: documentos relacionados
      /*descuento*/
      "descuento_select": listProducts[0].descuento.toString(),//TODO: Descuento por item

      "tipo_documento_seleccionado": tipoDocumento?.code,
      "condicion_operacion": condicionDeOperacion,
      "observaciones": observaciones,

      /*prodcutos*/
      "productos_ids": idListProducts,
      "cantidades": cantidadListProducts,
      "producto_id": idListProducts[0],
      "monto_fp": "1.42",
      "num_ref": null,

      /*retencion*/
      "retencion_iva": tieneRetencionIva,
      "porcentaje_retencion_iva": (retencionIva/100).toString,
      // "retencion_renta": false,
      // "porcentaje_retencion_renta": 0.00,

      /*tipos de pago*/
      "fp_id": formasPagoList,
    }
    console.log(data)

    try {
      const response = await generarFacturaService(data)
      console.log(response)
      console.log(response.factura_id)
      navigate(`/factura/${response.factura_id}`);

    }
    catch (error) {
      console.log(error)
    }
  }
  //************************************/
  // OBTENCION DE DATOS
  //************************************/
  useEffect(() => {
    fetchIdentificacionData()
  }, []);


  const fetchIdentificacionData = async () => {
    try {
      const response = await getFacturaCodigos()
      setCodigoGeneracion(response.codigo_generacion)
      setNumeroControl(response.numero_control)
      generarFactura();

    } catch (error) {
      console.log(error)
    }
  }

  const handleClickGenerarFactura = async () => {
    generarFactura()
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
            <DatosEmisorCard emisorData={emisorData} setEmisorData={setEmisorData} />
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
              <CheckBoxVentaTerceros />
              <CheckBoxRetencion setTieneRetencionIva={setTieneRetencionIva} setRetencionIva={setRetencionIva} retencionIva={retencionIva} tieneRetencionIva={tieneRetencionIva}/>
            </div>
          </div>
        </>
      </WhiteSectionsPage>

      {/*Seccion identificación*/}
      <WhiteSectionsPage>
        <div className="pt2 pb-5">
          <h1 className="text-start text-xl font-bold">Identificación</h1>
          <Divider className="m-0 p-0"></Divider>
          <IdentifcacionSeccion codigoGeneracion={codigoGeneracion} numeroControl={numeroControl}/>
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
            <TablaProductosAgregados listProducts={listProducts} setListProducts={setListProducts} setCantidadListProducts={setCantidadListProducts} setIdListProducts={setIdListProducts} setDescuentoItem={setDescuentoItem} descuentoItem={descuentoItem} />
            <ModalListaProdcutos
              visible={showProductsModal}
              setVisible={setShowProductsModal}
              setListProducts={setListProducts}
            />
            <FormasdePagoForm formasPagoList={formasPagoList} setFormasPagoList={setFormasPagoList} />
            <span className='flex flex-col justify-start items-start py-5'>
              <p className='opacity-70'>Observaciones</p>
              <div className="flex justify-content-center w-full">
                <InputTextarea autoResize value={observaciones} onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) => setObservaciones(e.target.value)} rows={3}  style={{width:'100%'}}/>
              </div>
            </span>
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
          <ResumenTotalesCard listProducts={listProducts} setDescuentoGeneral={descuentoGeneral} descuentoGeneral={descuentoGeneral}/>
        </div>
      </WhiteSectionsPage>

      <div className="mx-14 flex">
        <button
          type="button"
          className="bg-primary-yellow mb-5 self-start rounded-md px-5 py-3 text-white hover:cursor-pointer"
          onClick={handleClickGenerarFactura}
        >
          Generar factura
        </button>
      </div>
    </>
  );
};
