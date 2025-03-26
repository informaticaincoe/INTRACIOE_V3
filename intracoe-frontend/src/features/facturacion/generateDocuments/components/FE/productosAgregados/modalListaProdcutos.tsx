import { Divider } from 'primereact/divider';
import { Checkbox, CheckboxChangeEvent } from 'primereact/checkbox';
import { Column } from 'primereact/column';
import { DataTable } from 'primereact/datatable';
import { Dialog } from 'primereact/dialog';
import { useEffect, useState } from 'react';
import { defaultProductosData, ProductosTabla } from './productosData';
import { InputNumber, InputNumberValueChangeEvent } from 'primereact/inputnumber';
import { getAllProducts } from '../../../services/productos/productosServices';
import { SendFormButton } from '../../../../../../shared/buttons/sendFormButton';

interface ModalListProductsInterface {
  visible: any;
  setVisible: any;
  setListProducts:any;

}

export const ModalListaProdcutos: React.FC<ModalListProductsInterface> = ({
  visible,
  setVisible,
  setListProducts
}) => {
  const [products, setProducts] = useState<ProductosTabla[]>([defaultProductosData]);
  const [selectedProducts, setSelectedProducts] = useState<ProductosTabla[]>([]);

  useEffect(() => {
    fetchProductos()
  }, [])


  const fetchProductos = async () => {
    try {
      const response = await getAllProducts()
      const productos = response.map((product) => {
        const cantidadInicial = 1;
        const precioUnitario = product.preunitario;
        const ivaUnitario = precioUnitario * 0.12;
        const totalNeto = precioUnitario * cantidadInicial;
        const totalIVA = ivaUnitario * cantidadInicial;
        const totalConIVA = totalNeto + totalIVA;
      
        return {
          id: product.id,
          codigo: product.codigo,
          descripcion: product.descripcion,
          precio_unitario: precioUnitario,
          cantidad: cantidadInicial,
          no_grabado: false,
          descuento: 0,
          iva_unitario: ivaUnitario,
          total_neto: totalNeto,
          total_iva: totalIVA,
          iva_percibido: 0,
          total_tributos: 0,
          total_con_iva: totalConIVA,
          seleccionar: false,
        };
      });
      
      console.log("productos response", response)

      console.log("productos", productos)
 
      setProducts(productos)
    } catch (error) {
      console.log(error)
    }
  }

  // Función para manejar cambios en la cantidad
  const handleCantidadChange = (
    e: InputNumberValueChangeEvent,
    index: number
  ) => {
    const updatedProducts = [...products];
    const nuevaCantidad = e.value ?? 1;
    const producto = updatedProducts[index];
  
    producto.cantidad = nuevaCantidad;
    producto.total_iva = producto.iva_unitario * nuevaCantidad;
  
    setProducts(updatedProducts);
  };
  

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

  const guardarProductos =(selectedProducts:ProductosTabla[])=> {
    console.log(selectedProducts)
    setListProducts(selectedProducts)
  }

  const footerContent = (
    <div>
      <SendFormButton onClick={() => guardarProductos(selectedProducts)} text='Agregar' className='bg-primary-blue text-white px-10'/>

      <SendFormButton onClick={() => setVisible(false)} text='Cerrar' className='border border-primary-blue px-10'/>
        
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
          body={(rowData: ProductosTabla, { rowIndex }: any) => (
            <Checkbox
              checked={rowData.seleccionar} // Usa el estado de "seleccionar"
              onChange={(e) => handleSelectChange(e, rowIndex)} // Maneja el cambio solo para "seleccionar"
            />
          )}
          header={<p className="text-sm">SELECCIONAR</p>}
        />
        <Column
          body={(rowData: ProductosTabla) => <p>{rowData.descripcion}</p>}
          header={<p className="text-sm">PRODUCTOS</p>}
        />
        <Column
          body={(rowData: ProductosTabla) => <p>$ {rowData.precio_unitario}</p>}
          header={<p className="text-sm">PRECIO UNITARIO</p>}
        />
        <Column
          header={<p className="text-sm">CANTIDAD</p>}
          body={(rowData: ProductosTabla, { rowIndex }: any) => (
            <InputNumber
              value={rowData.cantidad}
              onValueChange={(e: InputNumberValueChangeEvent) => handleCantidadChange(e, rowIndex)}
              className="w-[5rem]"
              min={1}
            />
          )}
        />
      </DataTable>
    </Dialog>
  );
};
