
import { Column } from "primereact/column";
import { DataTable } from "primereact/datatable";
import { FcCancel } from "react-icons/fc";
import { TableListadoFacturasContainerProps } from "../../../../shared/interfaces/interfaces";
import { useEffect } from "react";

export const TableListadoFacturasContainer: React.FC<TableListadoFacturasContainerProps> = ({ data, pagination }) => {
  useEffect(()=>{
    console.log(pagination)
  },[])

  return (
    <div>
      <DataTable value={data} showGridlines tableStyle={{ minWidth: '50rem' }}>
        <Column header="Estado"
          body={(rowData: any) => (
            <>
              {rowData.recibido_mh == false && (
                <div className="flex gap-2 items-center">
                  <FcCancel />
                  <p className="text-red">Anulado</p>
                </div>
              )}
            </>
          )}
        />
        <Column field="numero_control" header="Numero de control" />
        <Column field="codigo_generacion" header="Código generación" />
        <Column field="fecha_emision" header="fecha emision" />
        <Column field="sello_recepcion" header="sello recepcion" />
        <Column header="Acciones"
          body={(rowData: any) => (
            <>
              <span className="flex flex-col gap-2 items-center">
                {/* { rowData.recibido_mh == true &&
                  <button className="border border-red-500 text-red-500 w-full rounded-md py-2">Anular</button>
                } */}
                <button className="border border-red-500 text-red-500 w-full rounded-md py-2">Anular</button>
                <button className="border border-gray-700 text-gray-700 w-full px-4 rounded-md py-2">Visualizar</button>
              </span>
            </>
          )}
        />
      </DataTable>

      <div className="pt-5">
        {/* <Paginator first={first} rows={rows} totalRecords={pagination.total} rowsPerPageOptions={[10, 20, 30]} onPageChange={onPageChange} /> */}
      </div>

    </div>
  );
};