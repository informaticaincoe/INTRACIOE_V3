import { Column } from 'primereact/column';
import { DataTable } from 'primereact/datatable';
import React, { useEffect } from 'react';
import { FaCheck } from 'react-icons/fa6';
import { FcCancel } from 'react-icons/fc';
import { RiSendPlaneFill } from 'react-icons/ri';
import styles from '../../style/ContingenciasTable.module.css';

interface TablaContainerContingenciasProps {
    contingenciasList: any;
    expandedRows: any;
    setExpandedRows: any;
    rowExpansionTemplate: any;
}

export const TablaContainerContingencias: React.FC<
    TablaContainerContingenciasProps
> = ({
    contingenciasList,
    expandedRows,
    setExpandedRows,
    rowExpansionTemplate,
}) => {

        useEffect(() => {
            console.log("**************", contingenciasList)
        }, [contingenciasList])
        return (
            <>
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
                                {rowData.recibido_mh ? (
                                    <FaCheck className="text-green" size={20} />
                                ) : (
                                    <FcCancel size={20} />
                                )}
                            </div>
                        )}
                    />
                    <Column
                        field="codigo_generacion"
                        header="Código generación"
                        bodyStyle={{ width: '20%' }}
                    />
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
                            <button className="bg-primary-blue rounded-md px-4 py-2 pr-4 text-white">
                                <span className="flex items-center justify-center gap-2">
                                    <RiSendPlaneFill />
                                    <span>Enviar</span>
                                </span>
                            </button>
                        )}
                    />
                </DataTable>
            </>
        );
    };
