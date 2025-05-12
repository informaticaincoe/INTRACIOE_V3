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
import { TablaProductosFacturaNotasDebito } from '../components/NotaDebito/TablaProductosFacturaNotasDebito';
import { SelectModeloFactura } from '../components/Shared/configuracionFactura/modeloDeFacturacion/selectModeloFactura';
import {
  ConfiguracionFacturaInterface,
  ReceptorDefault,
  defaultEmisorData,
  Descuentos,
  EmisorInterface,
  FacturaPorCodigoGeneracionResponse,
  ReceptorInterface,
  TipoDocumento,
  TipoDTE,
} from '../../../../shared/interfaces/interfaces';
import { ProductosTabla } from '../components/FE/productosAgregados/productosData';
import {
  FirmarFactura,
  generarAjusteService,
  generarNotaCreditoService,
  getFacturaBycodigo,
} from '../services/factura/facturaServices';
import { CheckBoxRetencion } from '../components/Shared/configuracionFactura/Retencion/checkBoxRetencion';
import { useFetcher, useNavigate } from 'react-router';
import { Input } from '../../../../shared/forms/input';
import { CheckboxBaseImponible } from '../components/Shared/configuracionFactura/baseImponible/checkboxBaseImponible';
import CustomToast, {
  CustomToastRef,
  ToastSeverity,
} from '../../../../shared/toast/customToast';
import { IoMdCloseCircle } from 'react-icons/io';
import { ExtensionCard } from '../components/Shared/entension/extensionCard';
import { ResumenCardNotaAjuste } from '../components/NotaDebito/resumenCardNotaAjuste';

export const GenerarDocumentosAjuste = () => {
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
  const [numeroControl, setNumeroControl] = useState('');
  const [codigoGeneracion, setCodigoGeneracion] = useState('');
  const [descuentosList, setDescuentosList] = useState();
  const [saldoFavor, setSaldoFavor] = useState<number>(0.0);

  //datos seleccionados para realizar la factura
  const [selectedCondicionDeOperacion, setSelectedCondicionDeOperacion] =
    useState<string>('1'); //id de la condicion de operacion (01 por defecto)
  const [selectedProducts, setSelectedProducts] = useState<ProductosTabla[]>(
    []
  ); //lista de productos que tendra la factura
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

  //calculos
  const [totalAPagar, setTotalAPagar] = useState<number>(0);
  const [auxManejoPagos, setAuxManejoPagos] = useState<number>(totalAPagar);
  const [facturasAjuste, setFacturasAjuste] = useState<
    FacturaPorCodigoGeneracionResponse[]
  >([]);
  const [baseImponible, setBaseImponible] = useState<boolean>(false);
  const [errorReceptor, setErrorReceptor] = useState<boolean>(false);
  const [errorFormasPago, setErrorFormasPago] = useState<boolean>(false);
  const [nombreResponsable, setNombreResponsable] = useState<string>('');
  const [docResponsable, setDocResponsable] = useState<string>('');
  const [tipoTransmision, setTipoTransmision] = useState<string>('');

  const [formData, setFormData] = useState({ codigo: '' });

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

  //Guardar datos en formData
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const generarFactura = async () => {
    const dataNCND = {
      tipoDocumento: tipoDocumentoSelected?.codigo,
      receptor_id: receptor.id,
      observaciones: observaciones,
      tipo_documento_seleccionado: tipoDocumentoSelected?.codigo ?? '05', //tipo DTE
      tipo_item_select: 1,
      documento_seleccionado: 2, // solo manjeo de documento electronico
      documento_relacionado:
        facturasAjuste[0]?.codigo_generacion.toUpperCase() ?? '',
      // descuento_select: descuentos,
      condicion_operacion: selectedCondicionDeOperacion, //contado, credito, otros
      porcentaje_retencion_iva: (retencionIva / 100).toString(),
      retencion_iva: retencionIva.toString(),
      productos_retencion_iva: '0.00',
      porcentaje_retencion_renta: '0.00',
      retencion_renta: '0.0',
      productos_retencion_renta: '0.00',
      num_ref: null,
      [tipoDocumentoSelected?.codigo === '05'
        ? 'productos_id_r'
        : 'productos_ids']: idListProducts,
      cantidades: cantidadListProducts, //cantidad de cada producto de la factura
      descuento_gravado: descuentos.descuentoGravado.toString(),
      descuento_global_input: descuentos.descuentoGeneral.toString(),
      contingencia: false,
      tipotransmision: tipoTransmision,
    };
    console.log('dataNCND', dataNCND);
    console.log('factura ajuste', facturasAjuste[0]);

    try {
      const response = await generarNotaCreditoService(dataNCND);
      firmarFactura(response.factura_id);
    } catch (error) {
      console.log(error);
    }
  };

  const firmarFactura = async (id: string) => {
    try {
      if (id) {
        await FirmarFactura(id);
        navigate(`/factura/${id}`);
      }
    } catch (error) {
      console.log(error);
    }
  };

  const fetchFacturaARelacionar = async () => {
    try {
      const response = await getFacturaBycodigo(formData.codigo);
      // Verificar si ya existe
      const yaExiste = facturasAjuste.some(
        (f) => f.codigo_generacion === response.codigo_generacion
      );
      if (yaExiste) return;
      // Inyectar propiedades adicionales en los productos
      const facturaProcesada: FacturaPorCodigoGeneracionResponse = {
        ...response,
        productos: response.productos.map((p) => ({
          ...p,
          cantidad_editada: p.cantidad, // **Agregar las cantidades editadas de cada producto
          monto_a_aumentar: 0, // **nuevo monto a modificar en el producto
        })),
      };

      setFacturasAjuste((prev) => [...prev, facturaProcesada]);
      setFormData({ codigo: '' }); // Limpiar input
    } catch (error: any) {
      handleAccion('error', <IoMdCloseCircle size={68} />, error.toString());
    }
  };

  /************************************/
  /* OBTENCION DE DATOS              
    /************************************/
  useEffect(() => {
    fetchfacturaData();
  }, []);

  useEffect(() => {
    fetchfacturaData();
  }, [tipoDocumentoSelected?.codigo]);

  const fetchfacturaData = async () => {
    try {
      const response = await generarAjusteService(
        tipoDocumentoSelected?.codigo ?? '05'
      );
      setCodigoGeneracion(response.codigo_generacion);
      setNumeroControl(response.numero_control);
      setEmisorData(response.emisor);
      setCondicionesOperacionList(response.tipooperaciones);
      setSelectedCondicionDeOperacion(response.tipooperaciones[0].codigo);
      setDescuentosList(response.descuentos);
      setTipoDocumento(response.tipoDocumentos);
      // setTipoDocumentoSelected(response.tipoDocumentos[0].codigo);
    } catch (error) {
      console.log(error);
    }
  };

  const handleClickGenerarFactura = async () => {
    if (auxManejoPagos != 0) {
      setErrorFormasPago(true);
      handleAccion(
        'error',
        <IoMdCloseCircle size={38} />,
        'No se ha realizado el pago completo'
      );
    }

    if (receptor.id == '') {
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
      <Title text="Generar ajustes" />
      {/* Seccion datos del emisor */}
      <WhiteSectionsPage>
        <>
          <div className="pt2 pb-5">
            <h1 className="text-start text-xl font-bold">Datos del emisor</h1>
            <Divider className="m-0 p-0"></Divider>
            <DatosEmisorCard emisorData={emisorData} />
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
                  setTipoDocumentoSelected={setTipoDocumentoSelected}
                  tipoDocumentoSelected={tipoDocumentoSelected}
                />
              </div>
              <SelectCondicionOperacion
                condicionesOperacionList={condicionesOperacionList}
                selectedCondicionDeOperacion={selectedCondicionDeOperacion}
                setSelectedCondicionDeOperacion={
                  setSelectedCondicionDeOperacion
                }
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
        </>
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

      <WhiteSectionsPage>
        <div className="pt-2 pb-5">
          <div className="flex justify-between">
            <h1 className="text-start text-xl font-bold text-nowrap">
              Ajustar factura
            </h1>
          </div>
          <Divider className="m-0 p-0" />
          <div className="flex items-center justify-between pb-5">
            <span className="flex w-full flex-wrap items-center justify-between gap-x-10 gap-y-5">
              <label htmlFor="tipoDocumentoGeneracion" className="text-nowrap">
                Tipo documento de generación:
                <span className="opacity-70"> Electronico</span>
              </label>
              {/* <DropFownTipoDeDocumentoGeneracion
                tipoGeneracionFactura={tipoGeneracionFactura}
                setTipoGeneracionFactura={setTipoGeneracionFactura}
              /> */}
              <span className="gap flex w-full items-center">
                <label htmlFor="codigo" className="text-nowrap">
                  Codigo de generacion:
                </label>
                <Input
                  name="codigo"
                  placeholder="codigo"
                  type="text"
                  className="mr-10 ml-3"
                  value={formData.codigo}
                  onChange={handleChange}
                />
              </span>
            </span>
            <button
              className="bg-primary-blue rounded-md px-5 py-3 text-nowrap text-white hover:cursor-pointer"
              onClick={() => fetchFacturaARelacionar()}
            >
              seleccionar factura
            </button>
          </div>
          {facturasAjuste && (
            <TablaProductosFacturaNotasDebito
              tipoDte={tipoDocumentoSelected?.codigo}
              setCantidadListProducts={setCantidadListProducts}
              facturasAjuste={facturasAjuste}
              setFacturasAjuste={setFacturasAjuste}
              setIdListProducts={setIdListProducts}
              setListProducts={setListProducts}
            />
          )}
        </div>
      </WhiteSectionsPage>

      {/*Seccion totales resumen*/}
      <WhiteSectionsPage>
        <div className="pt-2 pb-5">
          <div className="flex justify-between">
            <h1 className="text-start text-xl font-bold">Resumen de totales</h1>
          </div>
          <Divider className="m-0 p-0"></Divider>
          <ResumenCardNotaAjuste
            facturas={facturasAjuste}
            cantidades={cantidadListProducts}
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
    </>
  );
};
