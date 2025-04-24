import { useEffect, useState } from "react"
import { Title } from "../../../../shared/text/title"
import { GetAlEventosContingencia } from "../services/contingenciaService."
import { DataTable } from "primereact/datatable"
import { Column } from "primereact/column"
import { WhiteSectionsPage } from "../../../../shared/containers/whiteSectionsPage"
import { Contingencias, FilterContingencia } from "../interfaces/contingenciaInterfaces"
import { OptionsContainer } from "../componentes/filter/optionsContainer"
/* icons */
import { FaCheck } from "react-icons/fa6"
import { FcCancel } from "react-icons/fc"
import { RiSendPlaneFill } from "react-icons/ri";
/* css */
import styles from '../style/ContingenciasTable.module.css';
import { Accordion, AccordionTab } from "primereact/accordion"
import { Badge } from "primereact/badge"

const facturas = [
    {
        "id": 1,
        "tipo_dte": 1,
        "numero_control": "DTE-01-0000MOO1-000000000000025",
        "estado": false,
        "codigo_generacion": "1b19501b-2f12-46a7-baec-e9987aee0590",
        "sello_recepcion": null,
        "fecha_emision": "2025-02-19",
        "total_pagar": 1.41,
        "total_iva": 0.16,
        "recibido_mh": true,
        "estado_invalidacion": "Viva"
    },
    {
        "id": 2,
        "tipo_dte": 1,
        "numero_control": "DTE-01-0000MOO1-000000000000026",
        "estado": false,
        "codigo_generacion": "37bb4548-e58b-4762-9ac4-835563c7268f",
        "sello_recepcion": null,
        "fecha_emision": "2025-02-19",
        "total_pagar": "10.17",
        "total_iva": "1.17",
        "recibido_mh": false,
        "estado_invalidacion": "Viva"
    },
]

export const ContingenciasPage = () => {
    const [contingenciasList, setContingenciasList] = useState<Contingencias>()
    const [expandedRows, setExpandedRows] = useState<any[]>([]);

    const [filters, setFilters] = useState<FilterContingencia>({
        recibido_mh: null,
        sello_recepcion: null,
        has_sello_recepcion: null,
        tipo_dte: null
    });

    useEffect(() => {
        fetchContingencias()
    }, [])

    const fetchContingencias = async () => {
        try {
            const response = await GetAlEventosContingencia()
            setContingenciasList(response)
        } catch (error) {
            console.log(error)
        }
    }

    const rowExpansionTemplate = (data: any) => {
        return (
            <div className="w-full px-10 flex flex-col justify-center ">
                <Accordion multiple activeIndex={[0]} className={styles.customCollapse}>
                    <AccordionTab
                        header={
                            <span className={`flex items-center justify-between gap-2 w-full ${styles.customCollapse}`}>
                                <span className="font-bold white-space-nowrap">Lote 1</span>
                                <Badge value="2" />
                            </span>
                        }
                    >
                        <DataTable
                            value={facturas}
                            // style={{ width: '90%' }}
                            // tableStyle={{ minWidth: '80%' }}
                            className={styles.customSubTable}
                        >
                            <Column field="numero_control" header="Número de Control" />
                            <Column field="fecha_emision" header="Fecha Emisión" />
                            <Column field="total_pagar" header="Total a Pagar" />
                            <Column field="total_iva" header="IVA" />
                            <Column
                                header="Estado"
                                body={(rowData: any) =>
                                    rowData.recibido_mh ? <FaCheck className="text-green" /> : <FcCancel />
                                }
                            />
                        </DataTable>
                    </AccordionTab>
                    <AccordionTab
                        header={
                            <span className={`flex items-center justify-between gap-2 w-full ${styles.customCollapse}`}>
                                <span className="font-bold white-space-nowrap">Lote 1</span>
                                <Badge value="2" />
                            </span>
                        }
                    >
                        <DataTable
                            value={facturas}
                            // style={{ width: '90%' }}
                            // tableStyle={{ minWidth: '80%' }}
                            className={styles.customSubTable}
                        >
                            <Column field="numero_control" header="Número de Control" />
                            <Column field="fecha_emision" header="Fecha Emisión" />
                            <Column field="total_pagar" header="Total a Pagar" />
                            <Column field="total_iva" header="IVA" />
                            <Column
                                header="Estado"
                                body={(rowData: any) =>
                                    rowData.recibido_mh ? <FaCheck className="text-green" /> : <FcCancel />
                                }
                            />
                        </DataTable>
                    </AccordionTab>
                </Accordion>
            </div >
        );
    };

    return (
        <>
            <Title text="Listado de Facturas en Contiengencia" />
            <WhiteSectionsPage>
                <>
                    <OptionsContainer
                        total={contingenciasList?.count ?? 0}
                        setFilters={setFilters}
                        filters={filters}
                    />
                    <DataTable
                        value={contingenciasList?.results}
                        expandedRows={expandedRows}
                        onRowToggle={(e: any) => setExpandedRows(e.data)}
                        rowExpansionTemplate={rowExpansionTemplate}
                        dataKey="codigo_generacion"
                        tableStyle={{ minWidth: '100%' }}
                        className={styles.customTable}
                    >
                        <Column expander style={{ width: '3em' }} />
                        <Column
                            header="Estado"
                            body={(rowData: any) => (
                                <div className="flex items-center justify-center gap-1">
                                    {rowData.recibido_mh ? <FaCheck className="text-green" size={20} /> : <FcCancel size={20} />}
                                </div>
                            )}
                        />
                        <Column field="codigo_generacion" header="Código generación" bodyStyle={{ width: '20%' }} />
                        <Column
                            field="sello_recepcion"
                            header="Sello de recepción"
                            style={{ width: '20%' }}
                            bodyStyle={{
                                whiteSpace: 'normal',
                                wordBreak: 'break-word',
                                overflowWrap: 'break-word',
                            }}
                        />
                        <Column field="cantidad_lote" header="Cantidad lotes" />
                        <Column field="motivo_contingencia" header="Motivo de contingencia" />
                        <Column
                            header="Enviar contingencia"
                            body={() => (
                                <button className="bg-primary-blue text-white px-4 py-2 pr-4 rounded-md">
                                    <span className="flex gap-2 items-center justify-center">
                                        <RiSendPlaneFill />
                                        <span>Enviar</span>
                                    </span>
                                </button>
                            )}
                        />
                    </DataTable>

                </>
            </WhiteSectionsPage >
        </>
    )
}
