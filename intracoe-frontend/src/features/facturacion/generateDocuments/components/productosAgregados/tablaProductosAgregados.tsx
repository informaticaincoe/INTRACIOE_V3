import { Column } from 'primereact/column';
import { DataTable } from 'primereact/datatable';
import { Dialog } from 'primereact/dialog';
import { InputText } from 'primereact/inputtext';
import React, { useState } from 'react';
import { productosData } from './productosData';

interface Product {
    id: string;
    codigo: string;
    descripcion: string;
    precio_unitario: string;
    cantidad: string;
    no_grabado: boolean;
    descuento: number;
    iva_unitario: number;
    total_neto: number;
    total_iva: number;
    total_con_iva: number;
}

export const TablaProductosAgregados = ({ }) => {
    const [products, setProducts] = useState<Product[]>(productosData);

    // Función para manejar cambios en la cantidad
    const handleCantidadChange = (
        e: React.ChangeEvent<HTMLInputElement>,
        index: number
    ) => {
        const updatedProducts = [...products];
        updatedProducts[index].cantidad = e.target.value;
        setProducts(updatedProducts);
    };

    const handleDescuentoChange = (
        e: React.ChangeEvent<HTMLInputElement>,
        index: number
    ) => {
        const updatedProducts = [...products];
        updatedProducts[index].cantidad = e.target.value;
        setProducts(updatedProducts);
    };

    // Función para manejar cambios en el descuento
    const handleNoGrabadoChange = (
        e: React.ChangeEvent<HTMLInputElement>,
        index: number
    ) => {
        const updatedProducts = [...products];
        updatedProducts[index].no_grabado = e.target.checked; // Asignamos el valor booleano
        setProducts(updatedProducts);
    };

    return (
        <>
            <DataTable
                value={products}
                tableStyle={{ minWidth: '50rem' }}
                paginator
                rows={5}
                rowsPerPageOptions={[5, 10, 25, 50]}
            >
                <Column
                    field="descripcion"
                    header={<p className="text-sm">PRODUCTO</p>}
                ></Column>
                <Column
                    body={(rowData: Product) => <p>$ {rowData.precio_unitario}</p>}
                    header={<p className="text-sm">PRECIO UNITARIO</p>}
                ></Column>
                <Column
                    body={(rowData: Product) => <p>$ {rowData.precio_unitario}</p>}
                    header={<p className="text-sm">IVA UNITARIO</p>}
                ></Column>
                <Column
                    header={<p className="text-sm">CANTIDAD</p>}
                    body={(rowData: Product, { rowIndex }: any) => (
                        <InputText
                            type="number"
                            value={rowData.cantidad} // 'cantidad' es un string
                            onChange={(e) => handleCantidadChange(e, rowIndex)}
                            className="w-[5rem]"
                        />
                    )}
                />
                <Column
                    header={<p className="text-sm">DESCUENTO(%)</p>}
                    body={(rowData: Product, { rowIndex }: any) => (
                        <InputText
                            type="number"
                            value={rowData.descuento.toString()}
                            onChange={(e) => handleDescuentoChange(e, rowIndex)}
                            className="w-[5rem]"
                        />
                    )}
                ></Column>
                <Column
                    body={(rowData: Product) => <p>$ {rowData.total_neto}</p>}
                    header={<p className="text-sm">TOTAL NETO</p>}
                ></Column>
                <Column
                    body={(rowData: Product) => <p>$ {rowData.total_neto}</p>}
                    header={<p className="text-sm">TOTAL IVA</p>}
                ></Column>
                <Column
                    body={(rowData: Product) => <p>$ {rowData.total_con_iva}</p>}
                    header={<p className="text-sm">TOTAL CON IVA</p>}
                ></Column>
            </DataTable>
        </>
    );
};
