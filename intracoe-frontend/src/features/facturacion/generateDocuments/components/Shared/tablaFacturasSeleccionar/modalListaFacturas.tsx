import { Divider } from 'primereact/divider';
import { Checkbox, CheckboxChangeEvent } from 'primereact/checkbox';
import { Column } from 'primereact/column';
import { DataTable } from 'primereact/datatable';
import { Dialog } from 'primereact/dialog';
import { InputText } from 'primereact/inputtext';
import { useState } from 'react';
import { FacturaData } from './facturaData';

interface FacturaData {
  codigoGeneracion: string;
  numeroControl: string;
  fechaRemision: string;
  receptor: string;
  montoTotal: number;
  seleccionar: boolean;
}

interface ModalListfacturaInterface {
  visible: any;
  setVisible: any;
}

export const ModalListaFacturas: React.FC<ModalListfacturaInterface> = ({
  visible,
  setVisible,
}) => {
  const [factura, setfactura] = useState<FacturaData[]>(FacturaData);
  const [selectedfactura, setSelectedfactura] = useState<FacturaData[]>([]);

  // Función para manejar cambios en la cantidad
  // const handleCantidadChange = (
  //   e: React.ChangeEvent<HTMLInputElement>,
  //   index: number
  // ) => {
  //   const updatedfactura = [...factura];
  //   updatedfactura[index].cantidad = e.target.value;
  //   setfactura(updatedfactura);
  // };

  // Función para manejar la selección de productos
  const handleSelectChange = (
    e: CheckboxChangeEvent, // Cambiar el tipo del evento a CheckboxChangeEvent
    index: number
  ) => {
    const updatedfactura = [...factura];
    updatedfactura[index].seleccionar = e.checked ?? false; // Actualizar solo el valor de "seleccionar"
    setfactura(updatedfactura);

    // Filtramos los productos seleccionados (con seleccionar === true)
    const selected = updatedfactura.filter((product) => product.seleccionar);
    setSelectedfactura(selected); // Guardamos los productos seleccionados en la variable
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
        value={factura}
        tableStyle={{ minWidth: '50rem' }}
        paginator
        rows={5}
        rowsPerPageOptions={[5, 10, 25, 50]}
      >
        <Column
          body={(rowData: FacturaData, { rowIndex }: any) => (
            <Checkbox
              checked={rowData.seleccionar} // Usa el estado de "seleccionar"
              onChange={(e) => handleSelectChange(e, rowIndex)} // Maneja el cambio solo para "seleccionar"
            />
          )}
          header={<p className="text-sm">SELECCIONAR</p>}
        />
        <Column
          body={(rowData: FacturaData) => <p>{rowData.codigoGeneracion}</p>}
          header={<p className="text-sm">CÓDIGO DE GENERACIÓN</p>}
        />
        <Column
          body={(rowData: FacturaData) => <p>$ {rowData.numeroControl}</p>}
          header={<p className="text-sm">NÚMERO DE CONTROL</p>}
        />
        <Column
          header={<p className="text-sm">FECHA</p>}
          body={(rowData: FacturaData, { rowIndex }: any) => (
            <p>{rowData.fechaRemision}</p>
          )}
        />
        <Column
          header={<p className="text-sm">RECEPTOR</p>}
          body={(rowData: FacturaData, { rowIndex }: any) => (
            <p>{rowData.receptor}</p>
          )}
        />
        <Column
          header={<p className="text-sm">MONTO TOTAL</p>}
          body={(rowData: FacturaData, { rowIndex }: any) => (
            <p>{rowData.montoTotal}</p>
          )}
        />
      </DataTable>
    </Dialog>
  );
};
