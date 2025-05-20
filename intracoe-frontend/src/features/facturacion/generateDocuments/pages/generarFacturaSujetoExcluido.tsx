import { Divider } from 'primereact/divider';
import { WhiteSectionsPage } from '../../../../shared/containers/whiteSectionsPage';
import { useEffect, useRef, useState } from 'react';
import { SelectCondicionOperacion } from '../components/Shared/configuracionFactura/condicionOperacion/selectCondicionOperacion';
import { SelectTipoTransmision } from '../components/Shared/configuracionFactura/tipoTransmision/selectTipoTransmisión';
import { IdentifcacionSeccion } from '../components/Shared/identificacion.tsx/identifcacionSeccion';
import { FormasdePagoForm } from '../components/Shared/configuracionFactura/formasDePago/formasdePagoForm';
import { SelectModeloFactura } from '../components/Shared/configuracionFactura/modeloDeFacturacion/selectModeloFactura';
import { SendFormButton } from '../../../../shared/buttons/sendFormButton';
import {
    Descuentos,
} from '../../../../shared/interfaces/interfaces';
import { ProductosTabla } from '../components/FE/productosAgregados/productosData';
import { ResumenTotalesCard } from '../components/Shared/resumenTotales/resumenTotalesCard';
import { generarSujetoExcluidoService } from '../services/factura/facturaServices';
import { CheckBoxRetencion } from '../components/Shared/configuracionFactura/Retencion/checkBoxRetencion';
import { InputTextarea } from 'primereact/inputtextarea';
import { useNavigate } from 'react-router';
import CustomToast, {
    CustomToastRef,
    ToastSeverity,
} from '../../../../shared/toast/customToast';
import { IoMdCloseCircle } from 'react-icons/io';
import { ExtensionCard } from '../components/Shared/entension/extensionCard';
import { ProveedorResultInterface } from '../../../ventas/proveedores/interfaces/proveedoresInterfaces';
import { ContenedorTablaProveedores } from '../components/sujetoExcluido/proveedores/contenedorTablaProveedores';
import { ProductosProveedoresResults } from '../../../../shared/interfaces/interfaceFacturaJSON';
import { ContenedorTablaProductosPorProveedores } from '../components/sujetoExcluido/productosProveedor/contendorTablaProductosPorProveedor';
import { TablaTotalesSujetoExcluido } from '../components/sujetoExcluido/tablaResumen/tablaTotales';

interface GenerarFacturaSujetoExcluidoProps {
    tipoDocumentoSelected: any
    codigoGeneracion: any
    numeroControl: any
    condicionesOperacionList: any
    descuentosList: any
    tipoContibuyente: string
}

export const GenerarFacturaSujetoExcluido: React.FC<GenerarFacturaSujetoExcluidoProps> = ({ tipoDocumentoSelected, codigoGeneracion, numeroControl, condicionesOperacionList, tipoContibuyente }) => {
    //lista de datos obtenidas de la api
    const [selectedProveedores, setSelectedProveedores] = useState<ProveedorResultInterface>() // Varibale con proveedorSeleccionado

    const [descuentoGeneral, setDescuentoGeneral] = useState<number>(0);

    const [formasPagoList, setFormasPagoList] = useState<number[]>([]);

    //variables para mostrar modales
    const [showProductsModal, setShowProductsModal] = useState(false); //mostrar modal con lista de productos
    // const [visibleDocumentoRelacionadomodal, setVisibleDocumentoRelacionadomodal] = useState(false);

    //datos seleccionados para realizar la factura

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
    const [selectedCondicionDeOperacion, setSelectedCondicionDeOperacion] =
        useState<string>('1');

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
        console.log("selectedProducts", selectedProducts)
        selectedProducts.map((producto) => {

        })
    }, [selectedProducts])

    useEffect(() => {
        handleMontoPagar();
    }, [selectedProducts, idListProducts, cantidadListProducts, tieneRetencionIva, tieneRetencionRenta, descuentoGeneral]);

    // ...
    useEffect(() => {
        handleMontoPagar();
    }, [
        selectedProducts,
        cantidadListProducts,
        descuentoGeneral,
        tieneRetencionIva,
        tieneRetencionRenta,
    ]);

    const handleMontoPagar = () => {
        // 1) Calcula el subtotal: suma (precio × cantidad) – descuento por línea
        const subtotal = selectedProducts.reduce<number>((sum, prod, idx) => {
            const qty = parseFloat(cantidadListProducts[idx]) || 0;
            const baseLinea = prod.preunitario * qty;
            // Aquí usamos directamente el número que el usuario escribió en el input
            const descuentoLinea = prod.descuento?.id ?? 0;
            const totalLinea = baseLinea - descuentoLinea;
            return sum + totalLinea;
        }, 0);

        // 2) Aplica descuento general (si lo tienes)
        const montoDescuentoGeneral = subtotal * (descuentoGeneral / 100);
        const neto = subtotal - montoDescuentoGeneral;

        // 3) Retenciones
        const retRenta = tieneRetencionRenta ? neto * 0.10 : 0;
        const retIva = tieneRetencionIva ? neto * 0.13 : 0;

        // 4) Total final
        const total = parseFloat((neto - retRenta - retIva).toFixed(2));
        setTotalAPagar(total);
    };

    // ...

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
        const dataSujetoExcl = {
            receptor_id: selectedProveedores?.id,
            nit_receptor: selectedProveedores?.ruc_nit,
            nombre_receptor: selectedProveedores?.nombre,
            direccion_receptor: selectedProveedores?.direccion,
            telefono_receptor: selectedProveedores?.telefono,
            correo_receptor: selectedProveedores?.email,
            observaciones: observaciones,

            tipo_documento_seleccionado: tipoDocumentoSelected?.codigo ?? '14', //tipo DTE
            tipo_item_select: tipoItem,

            condicion_operacion: selectedCondicionDeOperacion, //contado, credito, otros

            /*** Sujeto excluido no aplica la retencion de IVA ***/
            porcentaje_retencion_iva: retencionIva.toString(),
            retencion_iva: tieneRetencionIva,

            porcentaje_retencion_renta: retencionRenta.toString(),
            retencion_renta: tieneRetencionRenta,
            // productos_retencion_renta
            fp_id: formasPagoList,

            descuento_global: descuentoGeneral.toString(),
            saldo_favor_input: saldoFavor,
            no_gravado: baseImponible,

            productos_ids: idListProducts,
            cantidades: cantidadListProducts, //cantidad de cada producto de la factura
            descuento_select: descuentosProducto, //lista de id de descuento

            monto_fp: totalAPagar.toFixed(2),
            num_ref: null,
            nombre_responsable: nombreResponsable || null,
            doc_responsable: docResponsable || null,
            tipotransmision: tipoTransmision,
        }
        console.log(dataSujetoExcl);

        try {
            const response = await generarSujetoExcluidoService(dataSujetoExcl);
            firmarFactura(response.factura_id);
        } catch (error) {
            console.log(error);
        }
    };

    const firmarFactura = async (id: string) => {
        try {
            if (id) {
                navigate(`/factura/${tipoDocumentoSelected?.codigo}/${id}`);
            }
        } catch (error) {
            console.log(error);
        }
    };

    /************************************/
    /* OBTENCION DE DATOS              
    /************************************/

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

        if (!selectedProveedores) {
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

    return (
        <>
            {/*Seccion configuración de factura*/}
            <WhiteSectionsPage>
                <div className="pt2 pb-5">
                    <h1 className="text-start text-xl font-bold">
                        Configuración factura
                    </h1>
                    <Divider className="m-0 p-0"></Divider>
                    <div className="flex flex-col gap-8">
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

                        <CheckBoxRetencion
                            tipoDocumentoSelected={tipoDocumentoSelected}
                            setTieneRetencionIva={setTieneRetencionIva}
                            tieneRetencionIva={tieneRetencionIva}
                            setRetencionIva={setRetencionIva}
                            retencionIva={retencionIva}
                            setTieneRetencionRenta={setTieneRetencionRenta}
                            tieneRetencionRenta={tieneRetencionRenta}
                            retencionRenta={retencionRenta}
                            setRetencionRenta={setRetencionRenta}
                            tipoContibuyente={tipoContibuyente}
                        />
                        {/* {tipoDocumentoSelected?.codigo != "14" && //Sujeto excluido no tiene base imponible
                            <CheckboxBaseImponible
                                baseImponible={baseImponible}
                                setBaseImponible={setBaseImponible}
                            />} */}
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
            {/* <WhiteSectionsPage>
                <div className="pt2 pb-5">
                    <>
                        <h1 className="text-start text-xl font-bold">
                            Sujeto excluido
                        </h1>
                        <Divider className="m-0 p-0"></Divider>
                        <>
                            <FormularioSujetoExcluido formData={formSujetoData} handleChange={undefined} />
                        </>
                    </>
                </div>
            </WhiteSectionsPage> */}

            {/*Seccion receptor*/}
            <WhiteSectionsPage>
                <div className="pt2 pb-5">
                    <>
                        <h1 className="text-start text-xl font-bold">
                            Seleccione el sujeto excluido
                        </h1>
                        <Divider className="m-0 p-0"></Divider>
                        {/* <ProveedoresPage mostrarTitulo={false} /> */}
                        <ContenedorTablaProveedores setSelectedProveedores={setSelectedProveedores} selectedProveedores={selectedProveedores} />

                    </>
                </div>
            </WhiteSectionsPage>

            {/* Seccion productos */}
            {/* Tipo de documento: FE y Credito fiscal */}
            <WhiteSectionsPage>
                <div className="pt-2 pb-5">
                    <div className="flex items-center justify-between">
                        <h1 className="text-start text-xl font-bold">
                            Agregar producto o servicio
                        </h1>
                        <span className="flex gap-4">
                            <SendFormButton
                                className="bg-primary-blue rounded-md px-5 text-nowrap text-white hover:cursor-pointer"
                                onClick={() => setShowProductsModal(true)}
                                text={'Añadir producto'}
                            />
                        </span>
                    </div>

                    <Divider />
                    <div className='text-start text-gray'>
                        {!selectedProveedores && (
                            <p>Seleccionar un proveedor</p>
                        )
                        }

                        {selectedProveedores && (
                            <ContenedorTablaProductosPorProveedores
                                selectedProveedores={selectedProveedores}
                                setSelectedProducts={setSelectedProducts}
                                selectedProducts={selectedProducts}
                                setCantidadListProducts={setCantidadListProducts}
                                setIdListProducts={setIdListProducts}
                                setDescuentoItem={setDescuentoItem}
                            />
                        )}


                    </div>
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
                    {/* <ResumenTotalesCard
                        tipoDocumento={tipoDocumentoSelected?.codigo ?? '01'}
                        setTotalAPagar={setTotalAPagar}
                        totalAPagar={totalAPagar}
                        listProducts={selectedProducts}
                        descuentos={descuentos}
                        setDescuentos={setDescuentos}
                        setSaldoFavor={setSaldoFavor}
                        saldoFavor={saldoFavor}
                    /> */}
                    <TablaTotalesSujetoExcluido
                        selectedProducts={selectedProducts}
                        cantidadListProducts={cantidadListProducts}
                        idListProducts={idListProducts}
                        descuentoGeneral={descuentoGeneral}
                        setDescuentoGeneral={setDescuentoGeneral}
                        totalAPagar={totalAPagar}
                        setTotalAPagar={setTotalAPagar}
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
