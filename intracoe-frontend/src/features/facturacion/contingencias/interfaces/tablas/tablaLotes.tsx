import { Accordion, AccordionTab } from 'primereact/accordion';
import { Badge } from 'primereact/badge';
import { Column } from 'primereact/column';
import { DataTable } from 'primereact/datatable';
import { FaCheck, FaCircleCheck } from 'react-icons/fa6';
import { FcCancel } from 'react-icons/fc';
import styles from '../../style/ContingenciasTable.module.css';
import React, { useEffect, useRef, useState } from 'react';
import {
  enviarFacturaContingencia,
  enviarLoteContingencia,
} from '../../services/contingenciaService.';
import CustomToast, {
  CustomToastRef,
  ToastSeverity,
} from '../../../../../shared/toast/customToast';
import { IoMdCloseCircle } from 'react-icons/io';
import { IoIosSend } from "react-icons/io";
import LoadingScreen from '../../../../../shared/loading/loadingScreen';

interface lotesInterface {
  codigo_generacion: string;
  facturas_en_grupos: any[];
  fecha_sello_recibido: string;
  id: number;
  mostrar_checkbox: boolean;
  motivo_contingencia: string | null;
  recibido_mh: boolean;
}
interface TablaLotesProps {
  lotes: lotesInterface;
  contingenciaEstado: any;
  updateContingencias: () => void;
}

export const TablaLotes: React.FC<TablaLotesProps> = ({
  lotes,
  contingenciaEstado,
  updateContingencias,
}) => {
  const [loading, setLoading] = useState(false)
  const toastRef = useRef<CustomToastRef>(null);

  useEffect(() => {
    console.log('66666666666666666666', lotes);
  }, [lotes]);

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

  // Helper to render a value or a hyphen if empty
  const renderValue = (value: any) =>
    value !== null && value !== undefined && value !== '' ? value : '-';

  const handleEnviarFactura = async (id: number) => {
    const data = {
      factura_id: id,
    };
    try {
      setLoading(true)
      await enviarFacturaContingencia(data);
      handleAccion(
        'success',
        <FaCircleCheck size={32} />,
        'Factura enviada con exito'
      );
      updateContingencias();
    } catch (error) {
      handleAccion(
        'error',
        <IoMdCloseCircle size={32} />,
        'Error al enviar la factura'
      );
    }
    finally {
      setLoading(false)
    }
  };

  const handleEnviarLote = async (id: any) => {
    const facturasList = lotes.facturas_en_grupos[id].facturas;
    const facturasListIds = facturasList.map((factura: any) => factura.id);

    const data = { factura_ids: facturasListIds };

    try {
      setLoading(true)
      await enviarLoteContingencia(data);
      handleAccion(
        'success',
        <FaCircleCheck size={32} />,
        'Factura enviada con exito'
      );
      updateContingencias();
    } catch (error) {
      handleAccion(
        'error',
        <IoMdCloseCircle size={32} />,
        'Error al enviar la factura'
      );
    }
    finally {
      setLoading(false)
    }
  };

  return (
    <>
      <CustomToast ref={toastRef} />
      {loading && <LoadingScreen />}

      <Accordion multiple className={styles.customCollapse}>
        {lotes.facturas_en_grupos.map((grupo, id) => {
          // 1) Todas facturas true
          const todasTrue = grupo.facturas.every(
            (f: { recibido_mh: boolean }) => f.recibido_mh === true
          );
          // 2) Todas facturas false
          const todasFalse = grupo.facturas.every(
            (f: { recibido_mh: boolean }) => f.recibido_mh === false
          );
          // 3) Facturas false y true
          const severity = todasTrue
            ? 'success'
            : todasFalse
              ? 'danger'
              : 'warning';

          return (
            <AccordionTab
              key={id}
              header={
                <div className="flex w-full items-center justify-between gap-2">
                  <span className="flex items-center gap-3">
                    <Badge
                      value={String(grupo.facturas.length)}
                      severity={severity}
                    />
                    <span className="font-bold">Lote {id + 1}</span>
                  </span>
                  {contingenciaEstado && (
                    <button
                      className="border-primary-blue hover:bg-primary-blue text-primary-blue flex items-center gap-2 rounded-md border px-5 py-2 font-medium hover:cursor-pointer hover:text-white"
                      onClick={(event) => {
                        handleEnviarLote(id)
                        event.stopPropagation()
                      }}
                    >
                      <IoIosSend size={24} />
                      <span>Enviar lote</span>
                    </button>
                  )}
                </div>
              }
            >
              <DataTable
                value={grupo.facturas}
                className={styles.customSubTable}
              >
                <Column
                  header="Numero control"
                  body={(row: any) => renderValue(row.numero_control)}
                />
                <Column
                  header="Sello recepción"
                  body={(row: any) => renderValue(row.sello_recepcion)}
                />
                <Column
                  header="Fecha Emisión"
                  body={(row: any) => renderValue(row.fecha_emision)}
                />
                <Column
                  header="Total a Pagar"
                  body={(row: any) => renderValue(row.total_pagar)}
                />
                <Column
                  header="IVA"
                  body={(row: any) => renderValue(row.total_iva)}
                />
                <Column
                  header="Estado"
                  body={(row: any) =>
                    row.recibido_mh ? (
                      <FaCheck className="text-green" />
                    ) : (
                      <FcCancel />
                    )
                  }
                />
                <Column
                  header="Acción"
                  body={(row: any) => {
                    if (!contingenciaEstado) return null;

                    return row.recibido_mh ? (
                      <FaCheck className="text-green" />
                    ) : (
                      <button
                        className="border-primary-blue hover:bg-primary-blue text-primary-blue flex items-center gap-2 rounded-md border px-5 py-2 font-medium hover:cursor-pointer hover:text-white"
                        onClick={() => handleEnviarFactura(row.id)}
                      >
                        <IoIosSend size={24} />
                        <span className="text-nowrap">Enviar factura</span>
                      </button>
                    );
                  }}
                />
              </DataTable>
            </AccordionTab>
          );
        })}
      </Accordion>
    </>
  );
};
