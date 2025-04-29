import { Column } from 'primereact/column';
import { DataTable } from 'primereact/datatable';
import React, { useEffect, useRef } from 'react';
import { FaCheck } from 'react-icons/fa6';
import { FcCancel } from 'react-icons/fc';
import { RiSendPlaneFill } from 'react-icons/ri';
import styles from '../../style/ContingenciasTable.module.css';
import { Paginator, PaginatorPageChangeEvent } from 'primereact/paginator';
import { enviarEventoContingencia } from '../../services/contingenciaService.';
import { FaCheckCircle } from 'react-icons/fa';
import CustomToast, { CustomToastRef, ToastSeverity } from '../../../../../shared/toast/customToast';
import { IoMdCloseCircle } from 'react-icons/io';

interface TablaContainerContingenciasProps {
    contingenciasList: any;
    expandedRows: any;
    setExpandedRows: any;
    rowExpansionTemplate: any;
    pagination: any;
    setPagination: any;
    onPageChange: (newPage: number) => void;
}

export const TablaContainerContingencias: React.FC<
    TablaContainerContingenciasProps
> = ({
    contingenciasList,
    expandedRows,
    setExpandedRows,
    rowExpansionTemplate,
    pagination,
    setPagination,
    onPageChange
    
}) => {
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

        const handleEnviarEventoContingencia = async (id: number) => {
            try {
                const
                    response = await enviarEventoContingencia(id)

                if (response.mesaje.contains('Error'))
                    handleAccion(
                        'error',
                        <IoMdCloseCircle size={38} />,
                        response.mensaje
                    );
                else
                    handleAccion(
                        'success',
                        <FaCheckCircle size={38} />,
                        response.mensaje
                    );
            } catch (error:any) {
                handleAccion(
                    'error',
                    <IoMdCloseCircle size={38} />,
                    "error" //TODO: validar si es error por que ya esta firmado
                );
            }
        }

        useEffect(() => {
            console.log("**************", pagination)
        }, [contingenciasList])
        return (
            <>
                <DataTable
                    value={contingenciasList?.results}
                    expandedRows={expandedRows}
                    onRowToggle={(e: any) => setExpandedRows(e.data)}
                    rowExpansionTemplate={rowExpansionTemplate}
                    dataKey="id"
                    tableStyle={{ minWidth: '100%', fontSize: '0.9em' }}
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
                        header="Codigo generacion"
                        body={(rowData: any) =>
                            rowData.codigo_generacion}
                        style={{ width: '20%' }}
                        bodyStyle={{
                            whiteSpace: 'normal',
                            wordBreak: 'break-word',
                            overflowWrap: 'break-word',
                        }}
                    />
                    <Column
                        header="Sello de recepción"
                        body={(rowData: any) =>
                            rowData.sello_recepcion !== null &&
                                rowData.sello_recepcion !== undefined &&
                                rowData.sello_recepcion !== ''
                                ? rowData.sello_recepcion
                                : '-'
                        }
                        style={{ width: '20%' }}
                        bodyStyle={{
                            whiteSpace: 'normal',
                            wordBreak: 'break-word',
                            overflowWrap: 'break-word',
                        }}
                    />
                    <Column
                        header="Cantidad lotes"
                        body={(rowData: any) =>
                            rowData.total_lotes_evento !== null &&
                                rowData.total_lotes_evento !== undefined &&
                                rowData.total_lotes_evento !== ''
                                ? rowData.total_lotes_evento
                                : '-'
                        }
                    />
                    <Column
                        header="Motivo de contingencia"
                        body={(rowData: any) =>
                            rowData.motivo_contingencia !== null &&
                                rowData.motivo_contingencia !== undefined &&
                                rowData.motivo_contingencia !== ''
                                ? rowData.motivo_contingencia
                                : '-'
                        }
                    />
                    <Column
                        header="Enviar contingencia"
                        body={(rowData: any) =>
                            rowData.mostrar_checkbox ? (
                                <button className="bg-primary-blue rounded-md px-4 py-2 text-white" onClick={() => handleEnviarEventoContingencia(rowData.id)}>
                                    <span className="flex items-center justify-center gap-2">
                                        <RiSendPlaneFill />
                                        <span>Enviar</span>
                                    </span>
                                </button>
                            ) : null
                        }
                    />
                </DataTable>
                <div className="pt-5">
                    <Paginator
                        first={(pagination.currentPage - 1) * pagination.pageSize}
                        rows={pagination.pageSize}
                        totalRecords={pagination.totalRecords}
                        rowsPerPageOptions={[10, 25, 50]}
                        onPageChange={(e: PaginatorPageChangeEvent) =>
                            onPageChange(e.page! + 1)
                          }
                    />
                </div>
                <CustomToast ref={toastRef} />

            </>
        );
    };
