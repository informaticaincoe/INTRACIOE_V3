import React, { useEffect, useState } from 'react'
import { AjusteInventarioInterface } from '../interfaces/ajusteInventarioInterfaces';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import { ModalDetalleAjusteMovimientoInventario } from './modalDetalleAjusteMovimientoInventario';

interface TablaAjusteInventarioProps {
    ajusteInventario: any
}
export const TablaAjusteInventario: React.FC<TablaAjusteInventarioProps> = ({ ajusteInventario }) => {
    const [visibleModal, setVisibleModal] = useState(false);
    const [selectedAjustesInventario, setSelectedAjustesInventario] = useState<AjusteInventarioInterface | null>(null);
    const [loading, setLoading] = useState(false)

    useEffect(() => {
        setVisibleModal(true)
        if (selectedAjustesInventario)
            console.log(selectedAjustesInventario)
    }, [selectedAjustesInventario])

    return (
        <>
            <DataTable
                value={ajusteInventario}
                tableStyle={{ minWidth: '50rem' }}
                selectionMode="single"
                selection={selectedAjustesInventario} // Se maneja como un único objeto de tipo movimientoInterface
                onSelectionChange={(e) => setSelectedAjustesInventario(e.value ? e.value as AjusteInventarioInterface : null)}
                dataKey="id"
            >
                <Column field="nombreProducto" header="Producto"></Column>
                <Column field="cantidad_ajustada" header="Cantidad"></Column>
                <Column field="fecha" header="Fecha"></Column>
                <Column field="nombreAlmacen" header="Almacen"></Column>
                <Column field="usuario" header="Usuario"></Column>
            </DataTable>

            {selectedAjustesInventario && (
                <ModalDetalleAjusteMovimientoInventario
                    data={selectedAjustesInventario} // Solo pasa un ID válido si hay un producto seleccionado
                    visible={visibleModal}
                    setVisible={setVisibleModal}
                />
            )}
        </>
    )
}
