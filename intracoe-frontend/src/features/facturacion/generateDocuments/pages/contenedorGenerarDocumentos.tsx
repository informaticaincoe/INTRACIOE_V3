import { useEffect, useRef, useState } from 'react'
import { Title } from '../../../../shared/text/title'
import { WhiteSectionsPage } from '../../../../shared/containers/whiteSectionsPage'
import { Divider } from 'primereact/divider'
import { DatosEmisorCard } from '../components/Shared/datosEmisor/datosEmisorCard'
import { ConfiguracionFacturaInterface, defaultEmisorData, EmisorInterface, TipoDocumento, TipoDTE } from '../../../../shared/interfaces/interfaces'
import { getFacturaCodigos, getFacturaCodigosSujetoExcluido } from '../services/factura/facturaServices'
import { ProductosTabla } from '../components/FE/productosAgregados/productosData'
import { useNavigate } from 'react-router'
import { CustomToastRef } from '../../../../shared/toast/customToast'
import { DropDownTipoDte } from '../components/Shared/configuracionFactura/tipoDocumento/DropdownTipoDte'
import { GenerarFacturaYCCF } from './generarFacturaYCCF'
import LoadingScreen from '../../../../shared/loading/loadingScreen'
import { GenerarFacturaSujetoExcluido } from './generarFacturaSujetoExcluido'
import { Proveedores } from '../../../../shared/interfaces/interfacesPagination'
import { GenerarFacturaExportacion } from './generarFacturaExportacion'

export const ContenedorGenerarDocumentos = () => {
    //lista de datos obtenidas de la api
    const [condicionesOperacionList, setCondicionesOperacionList] =
        useState<ConfiguracionFacturaInterface>();
    const [tipoDocumento, setTipoDocumento] = useState<TipoDocumento[]>([]); // almcenar tipo de dte
    const [tipoDocumentoSelected, setTipoDocumentoSelected] = useState<TipoDTE>(); // almcenar tipo de dte
    const [listProducts, setListProducts] = useState<ProductosTabla[]>([]); //lista que almacena todos los productos
    const [listProveedores, setListProveedores] = useState<Proveedores[]>([]); //lista que almacena todos los productos

    const [numeroControl, setNumeroControl] = useState('');
    const [codigoGeneracion, setCodigoGeneracion] = useState('');
    const [descuentosList, setDescuentosList] = useState();

    //datos seleccionados para realizar la factura
    const [selectedCondicionDeOperacion, setSelectedCondicionDeOperacion] =
        useState<string>('1'); //id de la condicion de operacion (01 por defecto)


    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();
    const toastRef = useRef<CustomToastRef>(null);

    const [emisorData, setEmisorData] = useState<EmisorInterface>(defaultEmisorData); // almcenar informacion del emisor

    useEffect(() => {
        const fetchTiposDocumento = async () => {
            try {
                const response = await getFacturaCodigos('01');

                setTipoDocumento(response.tipoDocumentos);

                // Establecer por defecto el primero si aún no está definido
                if (!tipoDocumentoSelected && response.tipoDocumentos.length > 0) {
                    setTipoDocumentoSelected(response.tipoDocumentos[0]);
                }
            } catch (error) {
                console.log(error);
            }
        };
        fetchTiposDocumento();
    }, []);

    useEffect(() => {
        console.log("tipo item codigo",tipoDocumentoSelected?.codigo)
        if (!tipoDocumentoSelected) return;
        
        console.log("otro")
        
        if (tipoDocumentoSelected.codigo == '14') {
            fetchFacturaDataSujeto()
        }

        console.log("otro")

        const fetchFacturaData = async () => {
            setLoading(true);
            try {
                const response = await getFacturaCodigos(tipoDocumentoSelected.codigo);

                setCodigoGeneracion(response.codigo_generacion);
                setNumeroControl(response.numero_control);
                setEmisorData(response.emisor);
                setCondicionesOperacionList(response.tipooperaciones);
                setSelectedCondicionDeOperacion(response.tipooperaciones[0].codigo);
                setDescuentosList(response.descuentos);
                setListProducts(response.producto);

                console.log("tipo dte selecionado", response)
            } catch (error) {
                console.log(error);
            } finally {
                setLoading(false);
            }
        };

        fetchFacturaData();
    }, [tipoDocumentoSelected]);

    const fetchFacturaDataSujeto = async () => {
        setLoading(true);
        try {
            const response = await getFacturaCodigosSujetoExcluido();

            setCodigoGeneracion(response.codigo_generacion);
            setNumeroControl(response.numero_control);
            setEmisorData(response.emisor);
            setCondicionesOperacionList(response.tipooperaciones);
            setSelectedCondicionDeOperacion(response.tipooperaciones[0].codigo);
            setDescuentosList(response.descuentos);
            setListProveedores(response.proveedores)

            console.log("tipo dte selecionado", response)
        } catch (error) {
            console.log(error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <>
            {loading && <LoadingScreen />}
            <Title text="Generar documentos" />

            {/* Seccion datos del emisor */}
            <WhiteSectionsPage>
                <div className="pt2 pb-5">
                    <h1 className="text-start text-xl font-bold">Datos del emisor</h1>
                    <Divider className="m-0 p-0"></Divider>
                    <DatosEmisorCard emisorData={emisorData} />
                </div>
            </WhiteSectionsPage>

            <WhiteSectionsPage>
                <div className="pt2 pb-5">
                    <h1 className="text-start text-xl font-bold">
                        Documento a generar
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

                    </div>
                </div>
            </WhiteSectionsPage>

            {
                (tipoDocumentoSelected?.codigo == '01' || tipoDocumentoSelected?.codigo == '03') &&
                <GenerarFacturaYCCF
                    tipoDocumentoSelected={tipoDocumentoSelected}
                    codigoGeneracion={codigoGeneracion}
                    numeroControl={numeroControl}
                    condicionesOperacionList={condicionesOperacionList}
                    descuentosList={descuentosList}
                    listProducts={listProducts}
                    tipoContibuyente={emisorData.tipoContibuyente}
                />
            }
            {
                (tipoDocumentoSelected?.codigo == '14') &&
                <GenerarFacturaSujetoExcluido
                    tipoDocumentoSelected={tipoDocumentoSelected}
                    codigoGeneracion={codigoGeneracion}
                    numeroControl={numeroControl}
                    condicionesOperacionList={condicionesOperacionList}
                    descuentosList={descuentosList}
                    tipoContibuyente={emisorData.tipoContibuyente}
                />
            }
            {
                (tipoDocumentoSelected?.codigo == '11') &&
                <GenerarFacturaExportacion
                    tipoDocumentoSelected={tipoDocumentoSelected}
                    codigoGeneracion={codigoGeneracion}
                    numeroControl={numeroControl}
                    condicionesOperacionList={condicionesOperacionList}
                    descuentosList={descuentosList}
                    tipoContibuyente={emisorData.tipoContibuyente}
                />
            }
        </>
    )
}

