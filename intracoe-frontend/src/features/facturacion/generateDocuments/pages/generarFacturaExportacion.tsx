import React, { useEffect, useState } from 'react'
import { WhiteSectionsPage } from '../../../../shared/containers/whiteSectionsPage'
import { Divider } from 'antd'
import { SelectModeloFactura } from '../components/Shared/configuracionFactura/modeloDeFacturacion/selectModeloFactura'
import { SelectTipoTransmision } from '../components/Shared/configuracionFactura/tipoTransmision/selectTipoTransmisión'
import { CheckBoxVentaTerceros } from '../components/Shared/configuracionFactura/ventaTerceros/checkboxVentaTerceros'
import { SelectTipoContingencia } from '../components/Shared/configuracionFactura/generacionEnContingencia/selectTipoContingencia'
import { MotivoContingencia } from '../components/Shared/configuracionFactura/generacionEnContingencia/motivoContingencia'
import { CheckboxDocumentosAsociados } from '../components/sujetoExcluido/otrosDocumentosAsociaidos/checkboxDocumentosAsociados'
import { OtrosDocumentosAsociados } from '../../../../shared/interfaces/interfaces'
import { Accordion, AccordionTab } from 'primereact/accordion'
import { FaTruck } from 'react-icons/fa6'
import { FaFileAlt } from 'react-icons/fa'
import { Badge } from 'primereact/badge'

interface GenerarFacturaExportacionProps {
    tipoDocumentoSelected: any
    codigoGeneracion: any
    numeroControl: any
    condicionesOperacionList: any
    descuentosList: any
    tipoContibuyente: string
}

const getIcon = (code: number) => {
    if (code === 4) return <FaTruck className="text-xl text-blue-600" />
    return <FaFileAlt className="text-xl text-green-600" />
}

const renderHeader = (doc: OtrosDocumentosAsociados) => (
    <div className="flex items-center justify-between w-full px-5">
        <div className="flex items-center gap-3">
            {getIcon(doc.codDocAsociado!)}
            <div>
                <h4 className="text-lg font-semibold">
                    {doc.descDocumento || `Documento ${doc.codDocAsociado}`}
                </h4>
                <small className="text-gray-500">Código: {doc.codDocAsociado}</small>
            </div>
        </div>
        <Badge
            value={doc.codDocAsociado === 4 ? 'Transporte' : 'Asociado'}
            severity={doc.codDocAsociado === 4 ? 'info' : 'success'}
            className="px-2 py-1"
        />
    </div>
)

const renderDetails = (doc: OtrosDocumentosAsociados) => (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 p-4 bg-gray-50 rounded">
        {['modoTransp', 'placaTrans', 'numConductor', 'nombreConductor', 'detalleDocumento'].map((field) => {
            const value = (doc as any)[field]
            if (!value) return null
            const labels: Record<string, string> = {
                modoTransp: 'Modo de transporte',
                placaTrans: 'Placa',
                numConductor: 'Cédula conductor',
                nombreConductor: 'Nombre conductor',
                detalleDocumento: 'Descripción',
            }
            return (
                <div key={field} className="flex flex-col">
                    <span className="text-sm text-gray-600">{labels[field]}</span>
                    <span className="font-medium">{value}</span>
                </div>
            )
        })}
    </div>
)


export const GenerarFacturaExportacion: React.FC<GenerarFacturaExportacionProps> = ({
    tipoDocumentoSelected,
    codigoGeneracion,
    numeroControl,
    condicionesOperacionList,
    descuentosList,
    tipoContibuyente,
}) => {
    const [tieneDocumentoAsociado, setTieneDocumentoAsociado] = useState<boolean>(false)

    /* variables api */
    const [tipoTransmision, setTipoTransmision] = useState<string>('');
    const [tipoModeloFacturacionSeleccionado, setTipoModeloFacturacionSeleccionado] = useState<any[]>([]); // TODO: Guardar el tipo de modelo
    const [tipoContingencia, setTipoContingencia] = useState<any>()
    const [motivo, setMotivo] = useState<string>('')
    const [documentosAsociadosLista, setDocumentosAsociadosLista] = useState<OtrosDocumentosAsociados[]>([])

    const [formDataDocumentosAsociados, setFormDataDocumentosAsociados] = useState<OtrosDocumentosAsociados>({
        codDocAsociado: null,
        descDocumento: null,
        detalleDocumento: null,
        modoTransp: null,
        placaTrans: null,
        numConductor: null,
        nombreConductor: null
    })

    /*************** Generar documento ***************/

    const handleClickGenerarFactura = async () => {

        const dataExportacion = {
            tipo_transmision_codigo: tipoTransmision,
            modelo_facturacion_codigo: tipoModeloFacturacionSeleccionado,
            tipo_contingencia_codigo: tipoContingencia,
            motivo: motivo
        };

        console.log(dataExportacion);

        // try {
        //     const response = await generarSujetoExcluidoService(dataExportacion);
        //     firmarFactura(response.factura_id);
        // } catch (error) {
        //     console.log(error);
        // }
    };

    /*************************************************/

    useEffect(() => {
        console.log("documentosAsociadosLista-------", documentosAsociadosLista)
        documentosAsociadosLista.forEach(element => (
            console.log("codigo:" + element.codDocAsociado)
        ))
    }, [documentosAsociadosLista])

    console.log(tipoDocumentoSelected)
    return (
        <>
            <WhiteSectionsPage>
                <div className="pt2 pb-5">
                    <h1 className="text-start text-xl font-bold">
                        Configuración factura
                    </h1>
                    <Divider className="m-0 p-0"></Divider>
                    <div className="flex flex-col gap-8">
                        <SelectModeloFactura
                            tipoModeloFacturacionSeleccionado={tipoModeloFacturacionSeleccionado}
                            setTipoModeloFacturacionSeleccionado={setTipoModeloFacturacionSeleccionado}
                        />
                        <SelectTipoTransmision
                            setTipoTransmision={setTipoTransmision}
                            tipoTransmision={tipoTransmision}
                        />

                        {tipoTransmision == '2' &&
                            <SelectTipoContingencia
                                setTipoContingencia={setTipoContingencia}
                                tipoContingencia={tipoContingencia}
                            />
                        }

                        {tipoContingencia == 5 &&
                            <MotivoContingencia
                                setMotivo={setMotivo}
                                motivo={motivo}
                            />
                        }

                        <CheckBoxVentaTerceros />
                    </div>


                </div>
            </WhiteSectionsPage>

            <WhiteSectionsPage>
                <>
                    <h1 className="text-start text-xl font-bold">
                        Documentos asociados
                    </h1>
                    <Divider className="m-0 p-0"></Divider>
                    <div className="flex flex-col gap-8">
                        <CheckboxDocumentosAsociados
                            tieneDocumentoAsociado={tieneDocumentoAsociado}
                            setTieneDocumentoAsociado={setTieneDocumentoAsociado}
                            setFormDataDocumentosAsociados={setFormDataDocumentosAsociados}
                            formDataDocumentosAsociados={formDataDocumentosAsociados}
                            setDocumentosAsociadosLista={setDocumentosAsociadosLista}
                            documentosAsociadosLista={documentosAsociadosLista}
                        />
                        {/* <Accordion multiple>
                            {
                                documentosAsociadosLista && (
                                    documentosAsociadosLista.map(element => (
                                        <AccordionTab
                                            style={{display:'flex', justifyContent:''}}
                                            header={
                                                <div className='text-start flex flex-col gap-4 px-5'>
                                                    {(element.codDocAsociado == 1 || element.codDocAsociado == 2) &&
                                                        <>
                                                            <p>Codigo: {element.codDocAsociado}</p>
                                                            <p>Identificación del documento: {element.descDocumento}</p>
                                                        </>
                                                    }
                                                    {(element.codDocAsociado == 4) &&
                                                        <>
                                                            <p>Codigo: {element.codDocAsociado}</p>
                                                            <p>Modo de transporte: {element.modoTransp}</p>
                                                        </>
                                                    }
                                                </div>
                                            }
                                        >
                                            {(element.codDocAsociado == 1 || element.codDocAsociado == 2) &&
                                                <div className='flex flex-col text-start gap-2'>
                                                    <p>Codigo: {element.codDocAsociado}</p>
                                                    <p>Identificación del documento: {element.descDocumento}</p>
                                                    <p>Descripción de documento asociado: {element.detalleDocumento}</p>
                                                </div>
                                            }
                                            {(element.codDocAsociado == 4) &&
                                                <div className='flex flex-col text-start gap-2'>
                                                    <p>Codigo: {element.codDocAsociado}</p>
                                                    <p>Modo de transporte: {element.modoTransp}</p>
                                                    <p>Numero de identificación del transporte: {element.placaTrans}</p>
                                                    <p>Número de identificación del conductor: {element.numConductor}</p>
                                                    <p>Nombre y apellidos del conductor: {element.nombreConductor}</p>
                                                </div>
                                            }
                                        </AccordionTab>
                                    ))
                                )
                            }
                        </Accordion> */}
                        {/* Accordion mejorado */}
                        <Accordion multiple className="shadow-sm border border-gray-200 rounded-lg overflow-hidden">
                            {documentosAsociadosLista.map((doc) => (
                                <AccordionTab key={doc.codDocAsociado} header={renderHeader(doc)}>
                                    {renderDetails(doc)}
                                </AccordionTab>
                            ))}
                        </Accordion>
                    </div>
                </>
            </WhiteSectionsPage >

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
    )
}
