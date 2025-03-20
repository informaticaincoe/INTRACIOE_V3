import { Column } from 'primereact/column';
import { DataTable } from 'primereact/datatable';
import { InputText } from 'primereact/inputtext';
import React, { useState } from 'react';
import { Product, productosData } from '../FE/productosAgregados/productosData';
import { Checkbox, CheckboxChangeEvent } from 'primereact/checkbox';
import { InputNumber, InputNumberValueChangeEvent } from 'primereact/inputnumber';

interface ProductosAAnular {
    id: string;
    montoAAnular: number;
}

export const TablaProductosFacturaNotasCredito = ({ }) => {
    const [products, setProducts] = useState<Product[]>(productosData);
    const [selectedProductos, setSelectedProductos] = useState<Product[]>([]); // Productos seleccionados
    const [descripcionAnulacion, setDescripcionAnulacion] = useState<{ [key: string]: string }>({}); // Descripciones por producto
    const [montoAAnular, setMontoAAnular] = useState<{ [key: string]: number }>({}); // Monto a anular por producto


    // Función para manejar cambios en la cantidad de un producto específico
    const handleCantidadChange = (value: number | null, productId: number) => {
        setProducts(prevProducts =>
            prevProducts.map(product =>
                product.id === productId ? { ...product, cantidad: value ?? 0 } : product
            )
        );
    };

    // Función para manejar cambios en la descripción de un producto
    const handleDescripcion = (value: React.ChangeEvent<HTMLInputElement>, productId: number) => {
        setDescripcionAnulacion(prev => ({
            ...prev,
            [productId]: value.target.value
        }));
    };

    // Función para manejar el monto a anular de un producto
    const handleMontoAAnularChange = (value: number | null, productId: number) => {
        setMontoAAnular(prev => ({
            ...prev,
            [productId]: value ?? 0
        }));
    };

    // Función para manejar la selección de productos
    const handleSelectChange = (e: CheckboxChangeEvent, productId: number) => {
        const updatedProducts = products.map(product =>
            product.id === productId
                ? { ...product, seleccionar: e.checked ?? false }
                : product
        );
        setProducts(updatedProducts);

        // Actualiza el estado de productos seleccionados
        if (e.checked) {
            const selectedProduct = products.find(p => p.id === productId);
            if (selectedProduct) {
                setSelectedProductos(prev => [...prev, selectedProduct]);
            }
        } else {
            setSelectedProductos(prev => prev.filter(p => p.id !== productId));
        }
    };

    // Función para obtener el monto total a anular solo de los productos seleccionados
    const totalMontoAAnular = () => {
        return products.reduce((total, product) => {
            if (product.seleccionar) {
                const monto = montoAAnular[product.id] ?? 0;
                return total + monto;
            }
            return total;
        }, 0);
    };

    const totalFactura = () => {
        return products.reduce((total, product) => {
            if (product.seleccionar) {
                const cantidad = product.cantidad ?? 0;
                const precio = parseFloat(product.precio_unitario) ?? 0;
                return total + (cantidad * precio);
            }
            return total;
        }, 0);
    };


    return (
        <>
            <div className='bg-gray-200 rounded-md py-8 px-14 opacity-80 mb-10'>
                <h1 className='font-bold text-xl text-start pb-8'>Factura</h1>
                <div className='grid grid-cols-[auto_1fr] text-start gap-x-10 gap-y-4'>
                    <p>Código generación:</p>
                    <p>e16394b2-2c23-4f7e-94be-d08b9ff17014</p>
                    <p>Número de control:</p>
                    <p>DTE-01-0000MOO1-000000000000095</p>
                    <p>Fecha emisión:</p>
                    <p>25/03/25    15:35</p>
                    <p>Receptor</p>
                    <p>Francisco Antonio Flores</p>
                    <p>Monto total</p>
                    <p>$150.00</p>
                </div>
            </div>
            <DataTable
                value={products}
                tableStyle={{ minWidth: '50rem' }}
                paginator
                rows={5}
                rowsPerPageOptions={[5, 10, 25, 50]}
            >
                <Column
                    body={(rowData: Product) => (
                        <Checkbox
                            checked={rowData.seleccionar}
                            onChange={(e) => handleSelectChange(e, rowData.id)}
                        />
                    )}
                    header={<p className="text-sm">SELECCIONAR</p>}
                />
                <Column
                    field="descripcion"
                    header={<p className="text-sm">PRODUCTO</p>}
                ></Column>

                <Column
                    body={(rowData: Product) => <p>$ {rowData.precio_unitario}</p>}
                    header={<p className="text-sm">PRECIO UNITARIO</p>}
                ></Column>
                <Column
                    header={<p className="text-sm">CANTIDAD</p>}
                    body={(rowData: Product) => (
                        <InputNumber
                            inputId="withoutgrouping"
                            value={rowData.cantidad}
                            onValueChange={(e: InputNumberValueChangeEvent) =>
                                handleCantidadChange(e.value ?? 0, rowData.id)
                            }

                        />
                    )}
                />
                <Column
                    header={<p className="text-sm">DESCRIPCION</p>}
                    body={(rowData: Product, { rowIndex }: any) => (
                        <InputText
                            type="text"
                            onChange={(e: React.ChangeEvent<HTMLInputElement>) => handleDescripcion(e, rowIndex)}
                            className="w-[15rem]"
                            disabled={!rowData.seleccionar}
                        />
                    )}
                />
                <Column
                    header={<p className="text-sm uppercase">monto a anular</p>}
                    body={(rowData: Product) => (
                        <InputNumber
                            value={montoAAnular[rowData.id] ?? 0}
                            onValueChange={(e: InputNumberValueChangeEvent) =>
                                handleMontoAAnularChange(e.value ?? 0, rowData.id)
                            }
                            disabled={!rowData.seleccionar}
                        />
                    )}
                />
            </DataTable>
            <div className='flex justify-between pt-10 items-start'>
                <button className='bg-primary-blue text-white rounded-md px-8 py-2 hover:cursor-pointer'>Factura completa</button>
                <span className='grid grid-cols-[auto_auto] gap-y-1 gap-x-10 text-end px-[5%]'>
                    <p className='font-semibold'>MONTO TOTAL A ANULAR</p>
                    <p>${totalMontoAAnular()}</p>
                    <p className='font-semibold'>MONTO TOTAL DE FACTURA</p>
                    <p>${totalFactura()}</p>
                </span>
            </div>
            <div className='flex flex-col justify-items-start items-start pt-5'>
                <p className='font-semibold'>Observaciones</p>
                <textarea className='border border-gray-300 rounded-md w-full h-28 text-start flex items-start py-3 px-5' />
            </div>
        </>
    );
};
