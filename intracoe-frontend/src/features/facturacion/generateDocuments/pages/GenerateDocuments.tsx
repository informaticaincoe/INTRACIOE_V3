import { Divider } from 'primereact/divider';
import { WhiteSectionsPage } from '../../../../shared/containers/whiteSectionsPage';
import { Title } from '../../../../shared/text/title';
import { useEffect, useRef, useState } from 'react';
import { DatosEmisorCard } from '../components/Shared/datosEmisor/datosEmisorCard';
import { DropDownTipoDte } from '../components/Shared/configuracionFactura/tipoDocumento/DropdownTipoDte';
import { SelectCondicionOperacion } from '../components/Shared/configuracionFactura/condicionOperacion/selectCondicionOperacion';
import { SelectTipoTransmision } from '../components/Shared/configuracionFactura/tipoTransmision/selectTipoTransmisión';
import { CheckBoxVentaTerceros } from '../components/Shared/configuracionFactura/ventaTerceros/checkboxVentaTerceros';
import { IdentifcacionSeccion } from '../components/Shared/identificacion.tsx/identifcacionSeccion';
import { SelectReceptor } from '../components/Shared/receptor/SelectReceptor';
import { ModalListaProdcutos } from '../components/FE/productosAgregados/modalListaProdcutos';
import { FormasdePagoForm } from '../components/Shared/configuracionFactura/formasDePago/formasdePagoForm';
import { SelectModeloFactura } from '../components/Shared/configuracionFactura/modeloDeFacturacion/selectModeloFactura';
import { SendFormButton } from '../../../../shared/buttons/sendFormButton';
import {
  ConfiguracionFacturaInterface,
  defaultEmisorData,
  Descuentos,
  EmisorInterface,
  ReceptorDefault,
  ReceptorInterface,
  TipoDocumento,
  TipoDTE,
} from '../../../../shared/interfaces/interfaces';
import { ProductosTabla } from '../components/FE/productosAgregados/productosData';
import { ResumenTotalesCard } from '../components/Shared/resumenTotales/resumenTotalesCard';
import {
  generarFacturaService,
  getFacturaCodigos,
} from '../services/factura/facturaServices';
import { CheckBoxRetencion } from '../components/Shared/configuracionFactura/Retencion/checkBoxRetencion';
import { InputTextarea } from 'primereact/inputtextarea';
import { useNavigate } from 'react-router';
import { CheckboxBaseImponible } from '../components/Shared/configuracionFactura/baseImponible/checkboxBaseImponible';
import CustomToast, {
  CustomToastRef,
  ToastSeverity,
} from '../../../../shared/toast/customToast';
import { IoMdCloseCircle } from 'react-icons/io';
import { TablaProductosAgregados } from '../components/FE/productosAgregados/tablaProductosAgregados';
import { ExtensionCard } from '../components/Shared/entension/extensionCard';
import LoadingScreen from '../../../../shared/loading/loadingScreen';

export const GenerateDocuments = () => {
  //lista de datos obtenidas de la api
  const [condicionesOperacionList, setCondicionesOperacionList] =
    useState<ConfiguracionFacturaInterface>();
  const [receptor, setReceptor] = useState<ReceptorInterface>(ReceptorDefault); // almacenar informacion del receptor
  const [emisorData, setEmisorData] =
    useState<EmisorInterface>(defaultEmisorData); // almcenar informacion del emisor
  const [tipoDocumento, setTipoDocumento] = useState<TipoDocumento[]>([]); // almcenar tipo de dte
  const [tipoDocumentoSelected, setTipoDocumentoSelected] = useState<TipoDTE>(); // almcenar tipo de dte

  const [descuentos, setDescuentos] = useState<Descuentos>({
    descuentoGeneral: 0,
    descuentoGravado: 0,
  });
  const [listProducts, setListProducts] = useState<ProductosTabla[]>([]); //lista que almacena todos los productos
  const [formasPagoList, setFormasPagoList] = useState<number[]>([]);

  const [numeroControl, setNumeroControl] = useState('');
  const [codigoGeneracion, setCodigoGeneracion] = useState('');
  const [descuentosList, setDescuentosList] = useState();

  //variables para mostrar modales
  const [showProductsModal, setShowProductsModal] = useState(false); //mostrar modal con lista de productos
  // const [visibleDocumentoRelacionadomodal, setVisibleDocumentoRelacionadomodal] = useState(false);

  //datos seleccionados para realizar la factura
  const [selectedCondicionDeOperacion, setSelectedCondicionDeOperacion] =
    useState<string>('1'); //id de la condicion de operacion (01 por defecto)
  const [selectedProducts, setSelectedProducts] = useState<ProductosTabla[]>(
    []
  );
  const [saldoFavor, setSaldoFavor] = useState<number>(0.0);

  //lista de productos que tendra la factura
  const [idListProducts, setIdListProducts] = useState<string[]>([]); // lista con solo los id de los productos que tendra la factura
  const [cantidadListProducts, setCantidadListProducts] = useState<string[]>(
    []
  );
  const [observaciones, setObservaciones] = useState<string>('');
  const [retencionIva, setRetencionIva] = useState<number>(0);
  const [retencionRenta, setRetencionRenta] = useState<number>(0);
  const [tieneRetencionIva, setTieneRetencionIva] = useState<boolean>(false);
  const [tieneRetencionRenta, setTieneRetencionRenta] =
    useState<boolean>(false);
  const [tipoItem, setTipoItem] = useState<number | null>(null);

  //calculos
  const [totalAPagar, setTotalAPagar] = useState<number>(0);
  const [auxManejoPagos, setAuxManejoPagos] = useState<number>(totalAPagar);
  const [descuentoItem, setDescuentoItem] = useState<number>(0);
  const [baseImponible, setBaseImponible] = useState<boolean>(false);
  const [errorReceptor, setErrorReceptor] = useState<boolean>(false);
  const [errorFormasPago, setErrorFormasPago] = useState<boolean>(false);
  const [nombreResponsable, setNombreResponsable] = useState<string>('');
  const [docResponsable, setDocResponsable] = useState<string>('');
  const [tipoTransmision, setTipoTransmision] = useState<string>('');
  const [descuentosProducto, setDescuentosProducto] = useState<number[]>([]);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const toastRef = useRef<CustomToastRef>(null);

  const handleAccion = (
    severity: ToastSeverity,
    icon: any,
    summary: string
  ) => {
    toastRef.current?.show({
      severity: severity,
      summary: summary,
      icon: icon,
      life: 2000,
    });
  };

  useEffect(() => {
    handleMontoPagar();
  }, [listProducts, idListProducts]);

  const handleMontoPagar = () => {
    let aux = 0;
    selectedProducts.map((pago) => {
      aux = aux + pago.total_con_iva;
    });
    setTotalAPagar(aux);
  };

  useEffect(() => {
    const descuentosAux: number[] = selectedProducts.map((producto) => {
      const porcentaje: number = producto.descuento?.id ?? 0;
      return Math.round(porcentaje * 100) / 100; // Redondea a 2 decimales
    });

    const tipoItemsList = selectedProducts.map(
      (producto) => producto.tipo_item
    );
    // Crear un set de los valores únicos
    const tipoItemsUnicos = new Set(tipoItemsList);
    if (tipoItemsUnicos.size === 1) {
      // Si todos los valores son iguales, asignar ese valor
      setTipoItem(tipoItemsList[0]);
    } else {
      // Si hay diferentes valores, asignar 3
      setTipoItem(3);
    }

    setDescuentosProducto(descuentosAux);
  }, [selectedProducts]);

  const generarFactura = async () => {
    const dataFECF = {
      // numero_control: numeroControl,
      receptor_id: receptor.id,
      nit_receptor: receptor.num_documento,
      nombre_receptor: receptor.nombre,
      direccion_receptor: receptor.direccion,
      telefono_receptor: receptor.telefono,
      correo_receptor: receptor.correo,
      observaciones: observaciones,

      tipo_documento_seleccionado: tipoDocumentoSelected?.codigo ?? '01', //tipo DTE
      tipo_item_select: tipoItem,

      condicion_operacion: selectedCondicionDeOperacion, //contado, credito, otros
      porcentaje_retencion_iva: retencionIva.toString(),
      retencion_iva: tieneRetencionIva,
      // productos_retencion_iva

      porcentaje_retencion_renta: retencionRenta.toString(),
      retencion_renta: tieneRetencionRenta,
      // productos_retencion_renta
      fp_id: formasPagoList,

      descuento_global_input: descuentos.descuentoGeneral.toString(),
      saldo_favor_input: saldoFavor,
      no_gravado: baseImponible,

      descuento_gravado: descuentos.descuentoGravado.toString(),

      productos_ids: idListProducts,
      cantidades: cantidadListProducts, //cantidad de cada producto de la factura
      descuento_select: descuentosProducto, //lista de id de desceun

      monto_fp: totalAPagar.toFixed(2),
      num_ref: null,
      nombre_responsable: nombreResponsable || null,
      doc_responsable: docResponsable || null,
      tipotransmision: tipoTransmision,
    };

    console.log(dataFECF);
    try {
      const response = await generarFacturaService(dataFECF);
      firmarFactura(response.factura_id);
    } catch (error) {
      console.log(error);
    }
  };

  const firmarFactura = async (id: string) => {
    try {
      if (id) {
        navigate(`/factura/${id}`);
      }
    } catch (error) {
      console.log(error);
    }
  };

  /************************************/
  /* OBTENCION DE DATOS              
  /************************************/
  useEffect(() => {
    fetchfacturaData();
  }, [tipoDocumentoSelected?.codigo]);

  const fetchfacturaData = async () => {
    setLoading(true);
    try {
      const response = await getFacturaCodigos(
        tipoDocumentoSelected?.codigo ?? '01'
      );
      setCodigoGeneracion(response.codigo_generacion);
      setNumeroControl(response.numero_control);
      setEmisorData(response.emisor);
      setCondicionesOperacionList(response.tipooperaciones);
      setSelectedCondicionDeOperacion(response.tipooperaciones[0].codigo);
      setDescuentosList(response.descuentos);
      setListProducts(response.producto);
      setTipoDocumento(
        response.tipoDocumentos.filter(
          (doc: { codigo: string }) =>
            doc.codigo === '01' || doc.codigo === '03'
        )
      );
    } catch (error) {
      console.log(error);
    } finally {
      setLoading(false);
    }
  };

  const handleClickGenerarFactura = async () => {
    if (auxManejoPagos != 0) {
      console.log('errpr pagos');
      setErrorFormasPago(true);
      handleAccion(
        'error',
        <IoMdCloseCircle size={38} />,
        'No se ha realizado el pago completo'
      );
    }

    if (receptor.id == '') {
      console.log('errpr receptr');

      setErrorReceptor(true);
      handleAccion(
        'error',
        <IoMdCloseCircle size={38} />,
        'Campo de receptor no debe estar vacio'
      );
    } else {
      generarFactura();
    }
  };

  //************************************/
  return (
    <>
      <Title text="Generar documentos" />
      {/* Seccion datos del emisor */}
      <WhiteSectionsPage>
        <div className="pt2 pb-5">
          <h1 className="text-start text-xl font-bold">Datos del emisor</h1>
          <Divider className="m-0 p-0"></Divider>
          <DatosEmisorCard emisorData={emisorData} />
        </div>
      </WhiteSectionsPage>

      {/*Seccion configuración de factura*/}
      <WhiteSectionsPage>
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
                setTipoDocumentoSelected={setTipoDocumentoSelected}
                tipoDocumentoSelected={tipoDocumentoSelected}
              />
            </div>
            <SelectCondicionOperacion
              condicionesOperacionList={condicionesOperacionList}
              selectedCondicionDeOperacion={selectedCondicionDeOperacion}
              setSelectedCondicionDeOperacion={setSelectedCondicionDeOperacion}
            />
            <SelectModeloFactura />
            <SelectTipoTransmision
              setTipoTransmision={setTipoTransmision}
              tipoTransmision={tipoTransmision}
            />
            <CheckBoxVentaTerceros />
            <CheckBoxRetencion
              setTieneRetencionIva={setTieneRetencionIva}
              tieneRetencionIva={tieneRetencionIva}
              setRetencionIva={setRetencionIva}
              retencionIva={retencionIva}
              setTieneRetencionRenta={setTieneRetencionRenta}
              tieneRetencionRenta={tieneRetencionRenta}
              retencionRenta={retencionRenta}
              setRetencionRenta={setRetencionRenta}
            />
            <CheckboxBaseImponible
              baseImponible={baseImponible}
              setBaseImponible={setBaseImponible}
            />
          </div>
        </div>
      </WhiteSectionsPage>

      {/*Seccion identificación*/}
      <WhiteSectionsPage>
        <div className="pt2 pb-5">
          <h1 className="text-start text-xl font-bold">Identificación</h1>
          <Divider className="m-0 p-0"></Divider>
          <IdentifcacionSeccion
            codigoGeneracion={codigoGeneracion}
            numeroControl={numeroControl}
          />
        </div>
      </WhiteSectionsPage>

      {/*Seccion receptor*/}
      <WhiteSectionsPage>
        <div className="pt2 pb-5">
          <h1 className="text-start text-xl font-bold">
            Seleccione el receptor
          </h1>
          <Divider className="m-0 p-0"></Divider>
          <SelectReceptor
            receptor={receptor}
            setReceptor={setReceptor}
            errorReceptor={errorReceptor}
            setErrorReceptor={setErrorReceptor}
          />
        </div>
      </WhiteSectionsPage>

      {/* Seccion productos */}
      {/* Tipo de documento: FE y Credito fiscal */}
      <WhiteSectionsPage>
        <div className="pt-2 pb-5">
          <div className="flex items-center justify-between">
            <h1 className="text-start text-xl font-bold">
              Productos agregados
            </h1>
            <span className="flex gap-4">
              {/* <ButtonDocumentosRelacionados
                visible={visibleDocumentoRelacionadomodal}
                setVisible={setVisibleDocumentoRelacionadomodal}
              /> */}
              <SendFormButton
                className="bg-primary-blue rounded-md px-5 text-nowrap text-white hover:cursor-pointer"
                onClick={() => setShowProductsModal(true)}
                text={'Añadir producto'}
              />
            </span>
          </div>

          <Divider />
          <TablaProductosAgregados
            // setSelectedProducts={setSelectedProducts}
            setListProducts={setSelectedProducts}
            listProducts={selectedProducts}
            setCantidadListProducts={setCantidadListProducts}
            setIdListProducts={setIdListProducts}
            setDescuentoItem={setDescuentoItem}
            descuentoItem={descuentoItem}
            descuentosList={descuentosList}
            tipoDte={tipoDocumentoSelected}
          />
          <ModalListaProdcutos
            tipoDte={tipoDocumentoSelected?.codigo ?? '01'}
            visible={showProductsModal}
            setVisible={setShowProductsModal}
            listProducts={listProducts}
            setSelectedProducts={setSelectedProducts}
            selectedProducts={selectedProducts}
          />
        </div>
      </WhiteSectionsPage>

      {/*Seccion formas de pago*/}
      <WhiteSectionsPage>
        <>
          <h1 className="text-start text-xl font-bold text-nowrap">
            Formas de pago
          </h1>
          <Divider />
          <FormasdePagoForm
            setFormasPagoList={setFormasPagoList}
            totalAPagar={totalAPagar}
            setErrorFormasPago={setErrorFormasPago}
            errorFormasPago={errorFormasPago}
            setAuxManejoPagos={setAuxManejoPagos}
            auxManejoPagos={auxManejoPagos}
          />
          <span className="flex flex-col items-start justify-start py-5 pt-10">
            <p className="opacity-70">Observaciones</p>
            <div className="justify-content-center flex w-full">
              <InputTextarea
                autoResize
                value={observaciones}
                onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) =>
                  setObservaciones(e.target.value)
                }
                rows={3}
                style={{ width: '100%' }}
              />
            </div>
          </span>
        </>
      </WhiteSectionsPage>

      {/*Seccion totales resumen*/}
      <WhiteSectionsPage>
        <div className="pt-2 pb-5">
          <div className="flex justify-between">
            <h1 className="text-start text-xl font-bold">Resumen de totales</h1>
          </div>
          <Divider className="m-0 p-0"></Divider>
          <ResumenTotalesCard
            tipoDocumento={tipoDocumentoSelected?.codigo ?? '01'}
            setTotalAPagar={setTotalAPagar}
            totalAPagar={totalAPagar}
            listProducts={selectedProducts}
            descuentos={descuentos}
            setDescuentos={setDescuentos}
            setSaldoFavor={setSaldoFavor}
            saldoFavor={saldoFavor}
          />
        </div>
      </WhiteSectionsPage>

      {totalAPagar > 25000 && (
        <WhiteSectionsPage>
          <div className="pt-2 pb-5">
            <div className="flex justify-between">
              <h1 className="text-start text-xl font-bold">Extensión</h1>
            </div>
            <Divider className="m-0 p-0"></Divider>
            <p className="text-red pb-10 text-start">
              * Campos obligatorios debido al monto de la factura
            </p>
            <ExtensionCard
              setNombreResponsable={setNombreResponsable}
              nombreResponsable={nombreResponsable}
              setDocResponsable={setDocResponsable}
              docResponsable={docResponsable}
            />
          </div>
        </WhiteSectionsPage>
      )}

      <div className="mx-14 flex">
        <button
          type="button"
          className="bg-primary-yellow mb-5 self-start rounded-md px-5 py-3 text-white hover:cursor-pointer"
          onClick={handleClickGenerarFactura}
        >
          Generar factura
        </button>
      </div>
      <CustomToast ref={toastRef} />
      {loading && <LoadingScreen />}
    </>
  );
};
