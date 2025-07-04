import { Pagination } from "../../../../../../shared/interfaces/interfacesPagination";
import { DataTable } from "primereact/datatable";
import { Column } from "primereact/column";
import { Paginator } from "primereact/paginator";
import { ProductosProveedorInterface } from "../../../../../../shared/interfaces/interfaceFacturaJSON";
import { useEffect } from "react";
import { Input } from "../../../../../../shared/forms/input";

interface TablaProductosPorProveedorSelectorProps {
    pagination: Pagination;
    onPageChange: (event: any) => void;
    productoProveedoresList: ProductosProveedorInterface | undefined;
    setSelectedProducts: (prods: any[]) => void;
    selectedProducts: any[];
    setCantidadListProducts: (cants: string[]) => void;
    setIdListProducts: (ids: string[]) => void;
}

export const TablaProductosPorProveedorSelector: React.FC<TablaProductosPorProveedorSelectorProps> = ({
    productoProveedoresList,
    pagination,
    onPageChange,
    selectedProducts,
    setSelectedProducts,
    setCantidadListProducts,
    setIdListProducts,
}) => {
    // Selección: inicializa cantidad y descuento cuando añades/quitas filas
    const onSelectionChange = (e: { value: any[] }) => {
        const nuevaSel = e.value;
        const merged = nuevaSel.map(item => {
            const prev = selectedProducts.find(p => p.id === item.id);
            return {
                ...item,
                cantidad: prev?.cantidad ?? 1,           // default 1
                descuento: prev?.descuento ?? { id: 0 }, // default 0%
            };
        });
        setSelectedProducts(merged);
    };

    // Cambiar cantidad
    const handleCantidadChange = (
        e: React.ChangeEvent<HTMLInputElement>,
        rowData: any
    ) => {
        const nuevaCant = parseInt(e.target.value, 10) || 0;
        const updated = selectedProducts.map(p =>
            p.id === rowData.id
                ? { ...p, cantidad: nuevaCant }
                : p
        );
        setSelectedProducts(updated);
    };

    // Cambiar descuento
    const handleDescuentoChange = (
        e: React.ChangeEvent<HTMLInputElement>,
        rowData: any
    ) => {
        const nuevoDesc = parseFloat(e.target.value) || 0;
        const updated = selectedProducts.map(p =>
            p.id === rowData.id
                ? { ...p, descuento: { ...p.descuento, id: nuevoDesc } }
                : p
        );
        setSelectedProducts(updated);
    };

    // Sincroniza arrays de ids y cantidades para el padre
    useEffect(() => {
        setIdListProducts(selectedProducts.map(p => String(p.id)));
        setCantidadListProducts(selectedProducts.map(p => String(p.cantidad ?? 0)));
    }, [selectedProducts]);

    return (
        <>
            <DataTable
                value={productoProveedoresList?.results}
                dataKey="id"
                selectionMode="multiple"
                metaKeySelection={false}
                selection={selectedProducts}
                onSelectionChange={onSelectionChange}
                tableStyle={{ minWidth: '50rem' }}
            >
                <Column selectionMode="multiple" headerStyle={{ width: '3rem' }} />
                <Column field="codigo" header="Código" />
                <Column field="descripcion" header="Descripción" />
                <Column field="preunitario" header="Precio unitario" />
                <Column field="tipo_item" header="Tipo" />

                <Column
                    header="Cantidad"
                    body={rowData => {
                        const sel = selectedProducts.find(p => p.id === rowData.id);
                        return (
                            <Input
                                name="cantidad"
                                type="number"
                                minNum={0}
                                step="1"
                                value={sel ? String(sel.cantidad) : '0'}
                                onChange={e => handleCantidadChange(e, rowData)}
                                className="w-16"
                            />
                        );
                    }}
                />

                <Column
                    header="Descuento (%)"
                    body={rowData => {
                        const sel = selectedProducts.find(p => p.id === rowData.id);
                        return (
                            <Input
                                name="descuento"
                                type="number"
                                minNum={0}
                                value={sel ? String(sel.descuento.id) : '0'}
                                onChange={e => handleDescuentoChange(e, rowData)}
                                className="w-20"
                            />
                        );
                    }}
                />
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
