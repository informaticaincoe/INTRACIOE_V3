import { Divider } from 'primereact/divider';
import { Checkbox, CheckboxChangeEvent } from 'primereact/checkbox';
import { Column } from 'primereact/column';
import { DataTable } from 'primereact/datatable';
import { Dialog } from 'primereact/dialog';
import { InputText } from 'primereact/inputtext';
import { useState } from 'react';
import { productosData } from './productosData';

interface Product {
    id: string;
    codigo: string;
    descripcion: string;
    precio_unitario: string;
    cantidad: string;
    no_grabado: boolean;
    seleccionar: boolean;
}

interface ModalListProductsInterface {
    visible: any;
    setVisible: any;
}

export const ModalListaProdcutos: React.FC<ModalListProductsInterface> = ({
    visible,
    setVisible,
}) => {
    const [products, setProducts] = useState<Product[]>(productosData);
    const [selectedProducts, setSelectedProducts] = useState<Product[]>([]);

    // Función para manejar cambios en la cantidad
    const handleCantidadChange = (
        e: React.ChangeEvent<HTMLInputElement>,
        index: number
    ) => {
        const updatedProducts = [...products];
        updatedProducts[index].cantidad = e.target.value;
        setProducts(updatedProducts);
    };

    // Función para manejar la selección de productos
    // Función para manejar la selección de productos
    const handleSelectChange = (
        e: CheckboxChangeEvent, // Cambiar el tipo del evento a CheckboxChangeEvent
        index: number
    ) => {
        const updatedProducts = [...products];
        updatedProducts[index].seleccionar = e.checked ?? false; // Actualizar solo el valor de "seleccionar"
        setProducts(updatedProducts);

        // Filtramos los productos seleccionados (con seleccionar === true)
        const selected = updatedProducts.filter((product) => product.seleccionar);
        setSelectedProducts(selected); // Guardamos los productos seleccionados en la variable
    };

    // Función para manejar el cambio de "No Grabado"
    const handleNoGrabadoChange = (
        e: CheckboxChangeEvent,  // Cambiar el tipo del evento a CheckboxChangeEvent
        index: number
    ) => {
        const updatedProducts = [...products];
        updatedProducts[index].no_grabado = e.checked ?? false;  // Actualizar solo el valor de "no_grabado"
        setProducts(updatedProducts);

        // Filtramos los productos seleccionados (con no_grabado === true)
        const selected = updatedProducts.filter((product) => product.no_grabado);
        setSelectedProducts(selected); // Guardamos los productos seleccionados en la variable
    };

    const footerContent = (
        <div>
            <button onClick={() => setVisible(false)} autoFocus>
                Close
            </button>
        </div>
    );

    return (
        <Dialog
            visible={visible}
            modal
            header={
                <>
                    <h1 className="text-start text-2xl font-bold">
                        Seleccionar productos
                    </h1>
                    <Divider className="m-0 p-0"></Divider>

                </>
            }
            footer={footerContent}
            style={{ width: '80%' }}
            onHide={() => setVisible(false)}
        >

            <DataTable
                value={products}
                tableStyle={{ minWidth: '50rem' }}
                paginator
                rows={5}
                rowsPerPageOptions={[5, 10, 25, 50]}
            >
                <Column
                    body={(rowData: Product, { rowIndex }: any) => (
                        <Checkbox
                            checked={rowData.seleccionar} // Usa el estado de "seleccionar"
                            onChange={(e) => handleSelectChange(e, rowIndex)} // Maneja el cambio solo para "seleccionar"
                        />
                    )}
                    header={<p className="text-sm">SELECCIONAR</p>}
                />
                <Column
                    body={(rowData: Product) => <p>{rowData.descripcion}</p>}
                    header={<p className="text-sm">PRODUCTOS</p>}
                />
                <Column
                    body={(rowData: Product) => <p>$ {rowData.precio_unitario}</p>}
                    header={<p className="text-sm">PRECIO UNITARIO</p>}
                />
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
                    body={(rowData: Product, { rowIndex }: any) => (
                        <Checkbox
                            checked={rowData.no_grabado} // Usa el estado de "no grabado"
                            onChange={(e) => handleNoGrabadoChange(e, rowIndex)} // Maneja el cambio solo para "no grabado"
                        />
                    )}
                    header={<p className="text-sm">NO GRABADO</p>}
                />
            </DataTable>
        </Dialog>
    );
};
