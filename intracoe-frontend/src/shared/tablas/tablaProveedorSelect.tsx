import React, { useEffect, useState } from 'react';
import { useSearchParams } from 'react-router';
import { ProveedorInterface } from '../../features/ventas/proveedores/interfaces/proveedoresInterfaces';
import { Pagination } from '../interfaces/interfacesPagination';
import { getAllProveedores } from '../../features/ventas/proveedores/services/proveedoresServices';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import { Paginator } from 'primereact/paginator';
import { Dialog } from 'primereact/dialog';

interface TableProveedorselectInterface {
  visible: boolean;
  setVisible: any;
  setSelectedProveedores: any;
  selectedProveedores: any;
  handleChange: any;
}

export const TablaProveedorSelect: React.FC<TableProveedorselectInterface> = ({
  visible,
  setVisible,
  setSelectedProveedores,
  selectedProveedores,
  handleChange,
}) => {
  const [selectedProducts, setSelectedProducts] = useState<any[]>([]);
  const [rowClick] = useState<boolean>(true);
  const [searchParams, setSearchParams] = useSearchParams();
  const [loading, setLoading] = useState(false);
  const [proveedorList, setProveedorList] = useState<ProveedorInterface>({
    count: 1,
    current_page: 1,
    page_size: 10,
    has_next: true,
    has_previous: false,
    results: [],
  });
  const [codigoFiltro, setCodigoFiltro] = useState<string>('');
  const [pagination, setPagination] = useState<Pagination>({
    count: 1,
    current_page: 1,
    page_size: 5,
    has_next: true,
    has_previous: false,

  });

  useEffect(() => {
    console.log("SSSSSSSSSSSSSSSSSSS", selectedProducts)
  }, [selectedProducts]);


  useEffect(() => {
    fetchProveedores();
  }, []);

  useEffect(() => {
    // Reinicia a la página 1 cada vez que los filtros cambian
    setPagination((prev) => ({ ...prev, current_page: 1 }));
    // Se utiliza el page_size actual para la consulta
    fetchProveedores(1, pagination.page_size); //enviar el numero de pagina actual 1 por defecto, enviar la cantidad de elementos en pagina
  }, []);

  const onPageChange = (event: any) => {
    const page = event.page + 1;
    const limit = event.rows;
    fetchProveedores(page, limit);
  };

  const fetchProveedores = async (page = 1, limit = 10) => {
    try {
      setLoading(true);
      const response = await getAllProveedores({ page, limit });
      if (response) {
        setProveedorList(response);
        setPagination({
          count: response.count || 0,
          current_page: response.current_page || 1,
          page_size: response.page_size || limit,
          has_next: response.has_next,
          has_previous: response.has_previous,
        });

        const params: Record<string, string> = {
          page: String(response.current_page),
          page_size: String(response.page_size),
          // date_from: initialDateFrom,        // <-- futuro: filtro fecha
          // date_to:   initialDateTo,
        };
        setSearchParams(params, { replace: true });
      } else {
        setPagination({
          count: 1,
          current_page: 1,
          page_size: 5,
          has_next: true,
          has_previous: false,
        });
      }
    } catch (error) {
      console.log(error);
    }
  };

  const handleSearch = (nuevoCodigo: string) => {
    setCodigoFiltro(nuevoCodigo.trim());
  };

  return (
    <>
      <Dialog
        header={
          <div className="flex justify-between">
            <p>Lista proveedores</p>
            <button
              onClick={() => setVisible(false)}
              className="bg-primary-blue mr-2 rounded-md px-5 py-2 text-[1rem] font-normal text-white"
            >
              Guardar seleccion
            </button>
          </div>
        }
        visible={visible}
        style={{ width: '70vw' }}
        onHide={() => {
          if (!visible) return;
          setVisible(false);
        }}
      >
        <DataTable
          value={proveedorList.results}
          tableStyle={{ minWidth: '100%' }}
          selectionMode="single"
          selection={selectedProveedores}
          onSelectionChange={(e) => {
            setSelectedProveedores(e.value);
            handleChange({
              target: { name: 'proveedor', value: e.value.id },
            });
          }}
        >
          <Column
            selectionMode="single"
            headerStyle={{ width: '3rem' }}
          ></Column>
          <Column field="nombre" header="Nombre"></Column>
          <Column field="correo" header="Correo"></Column>
          <Column field="ruc_nit" header="Nit/ruc"></Column>

          <Column
            field="condiciones_pago"
            header="Condiciones de pago"
          ></Column>
        </DataTable>
        <div className="pt-5">
          <Paginator
            first={(pagination.current_page - 1) * pagination.page_size}
            rows={pagination.page_size}
            totalRecords={pagination.count}
            rowsPerPageOptions={[5, 10, 25, 50]}
            onPageChange={onPageChange}
          />
        </div>
      </Dialog>
    </>
  );
};
