import { Column } from 'primereact/column';
import { DataTable } from 'primereact/datatable';
import { TableListadoFacturasContainerProps } from '../../../../shared/interfaces/interfaces';
import { Paginator } from 'primereact/paginator';

import { RiBillLine } from 'react-icons/ri';
import { FaCheck } from 'react-icons/fa6';
import { BsHourglassSplit } from 'react-icons/bs';
import { AiFillSignature } from 'react-icons/ai';
import { FcCancel } from 'react-icons/fc';

import { invalidarDte } from '../services/listadoFacturasServices';
import { useNavigate } from 'react-router';
import { Tooltip } from 'antd';

export const TableListadoFacturasContainer: React.FC<
  TableListadoFacturasContainerProps
> = ({ data, pagination, onPageChange }) => {
  const navigate = useNavigate();

  const visualizarFactura = async (id: number) => {
    try {
      navigate(`/factura/${id}`);
    } catch (error) {
      console.log(error);
    }
  };

  const invalidarFactura = async (id: number) => {
    try {
      const response = await invalidarDte(id);
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <div>
      <DataTable
        value={data}
        showGridlines
        tableStyle={{ minWidth: '50rem' }}
        emptyMessage="0 facturas"
      >
        <Column
          header="Estado"
          body={(rowData: any) => (
            <>
              <div className="flex items-center justify-start gap-1">
                {rowData.estado_invalidacion == 'Viva' &&
                  rowData.recibido_mh == true && ( //Sin invalidacion y recibida en hacienda esta enviado correctamente
                    <>
                      <FaCheck className="text-green" />
                      <p className="text-green">Enviado</p>
                    </>
                  )}
                {rowData.estado_invalidacion == 'Viva' &&
                  !rowData.recibido_mh && ( //Sin invalidacion y sin recibirse en hacienda (falta publicar)
                    <>
                      <AiFillSignature size={24} className="text-gray" />
                      <p className="text-gray">Envio pendiente</p>
                    </>
                  )}
                {rowData.estado_invalidacion == 'Invalidada' && ( //estado invalidado (invalidado)
                  <>
                    <FcCancel />
                    <p className="text-red">Anulado</p>
                  </>
                )}
                {rowData.estado_invalidacion ==
                  'En proceso de invalidación' && ( //estado en proceso de invalidacion (en proceso)
                  <>
                    <BsHourglassSplit
                      className="text-primary-yellow"
                      size={24}
                    />
                    <p className="text-primary-yellow">Invalidando</p>
                  </>
                )}
                {/* !estado && !sello no enviado */}
              </div>
            </>
          )}
        />
        <Column field="numero_control" header="Numero de control" />
        <Column field="codigo_generacion" header="Código generación" />
        <Column field="fecha_emision" header="fecha emision" />
        <Column
          header="Sello recepcion"
          style={{ width: '15vw', wordWrap: 'break-word' }}
          body={(rowData: any) => (
            <p className="w-[15vw] text-wrap">{rowData.sello_recepcion}</p>
          )}
        />
        <Column
          header="Acciones"
          body={(rowData: any) => (
            <>
              <span className="flex items-center gap-2">
                {rowData.estado_invalidacion == 'Viva' && (
                  <>
                    <Tooltip title="Anular">
                      <button
                        className="flex w-full cursor-pointer items-center gap-1 text-red-500"
                        onClick={() => invalidarFactura(rowData.id)}
                      >
                        <FcCancel size={22} />
                      </button>
                    </Tooltip>
                  </>
                )}
                <Tooltip className="visualizar">
                  <button
                    className="flex w-full cursor-pointer items-center gap-1 rounded-md text-gray-700"
                    onClick={() => visualizarFactura(rowData.id)}
                  >
                    <RiBillLine size={22} />
                  </button>
                </Tooltip>
              </span>
            </>
          )}
        />
      </DataTable>

      <div className="pt-5">
        <Paginator
          first={(pagination.current_page - 1) * pagination.page_size}
          rows={pagination.page_size}
          totalRecords={pagination.total_records}
          rowsPerPageOptions={[10, 25, 50]}
          onPageChange={onPageChange}
        />
      </div>
    </div>
  );
};
