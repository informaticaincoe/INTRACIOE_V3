import { Pagination } from "../../../../../../shared/interfaces/interfacesPagination";
import { ProveedorResultInterface } from "../../../../../ventas/proveedores/interfaces/proveedoresInterfaces";
import { DataTable } from "primereact/datatable";
import { Column } from "primereact/column";
import { Paginator } from "primereact/paginator";

interface TablaProveedoresSelectorProps {
    pagination: Pagination;
    onPageChange: (event: any) => void;
    proveedoresList: ProveedorResultInterface[] | undefined;
    updateList: () => void;
    selectedProveedores: any;
    setSelectedProveedores: any;
}

export const TablaProveedoresSelectorSelector: React.FC<TablaProveedoresSelectorProps> = ({
    proveedoresList,
    updateList,
    pagination,
    onPageChange,
    selectedProveedores,
    setSelectedProveedores,
}) => {

    return (
        <>
            <DataTable
                value={proveedoresList}
                tableStyle={{ minWidth: '50rem' }}
                selectionMode='single'
                selection={selectedProveedores!}
                onSelectionChange={(e: { value: React.SetStateAction<any[]> }) =>
                    setSelectedProveedores(e.value)
                }
            >
                <Column
                    selectionMode="single"
                    headerStyle={{ width: '3rem' }}
                ></Column>
                <Column field="nombre" header="Nombre"></Column>
                <Column field="ruc_nit" header="Nit/ruc"></Column>
                <Column field="telefono" header="Telefono"></Column>
                <Column field="email" header="Correo"></Column>
                
            </DataTable>
            <div className="pt-5">
                <Paginator
                    first={(pagination.current_page - 1) * pagination.page_size}
                    rows={pagination.page_size}
                    totalRecords={pagination.count}
                    onPageChange={onPageChange}
                />
            </div>
        </>
    );
};
