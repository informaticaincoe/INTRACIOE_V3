import React, { useEffect, useState } from 'react';
import { Title } from '../../../../shared/text/title';
import { WhiteSectionsPage } from '../../../../shared/containers/whiteSectionsPage';
import { Divider } from 'primereact/divider';
import { TablaProveedores } from '../componentes/tablaProveedores';
import { ProveedorInterface } from '../interfaces/proveedoresInterfaces';
import { getAllProveedores } from '../services/proveedoresServices';
import { TablaProveedoresHeader } from '../componentes/tablaProveedoresHeader';
import { useSearchParams } from 'react-router';
import { Pagination } from '../../../../shared/interfaces/interfacesPagination';


export const ProveedoresPage = () => {
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
    page_size: 10,
    has_next: true,
    has_previous: false,
  });

  useEffect(() => {
    fetchProveedores();
  }, []);

  useEffect(() => {
    setPagination((prev) => ({ ...prev, current_page: 1 }));
    fetchProveedores(1, pagination.page_size); //enviar el numero de pagina actual 1 por defecto, enviar la cantidad de elementos en pagina
  }, []);

  const updateCompras = () => {
    fetchProveedores(pagination.current_page);
  };

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
          page_size: 10,
          has_next: true,
          has_previous: false,
        });
      }
    } catch (error) {
      console.log(error);
    }
  };

  const updateList = () => {
    fetchProveedores();
  };

  const handleSearch = (nuevoCodigo: string) => {
    setCodigoFiltro(nuevoCodigo.trim());
  };

  return (
    <>
      <Title text={'Proveedores'} />

      <WhiteSectionsPage>
        <>
          <TablaProveedoresHeader
            codigo={codigoFiltro}
            onSearch={handleSearch}
          />
          <Divider />
          <TablaProveedores
            pagination={pagination}
            onPageChange={onPageChange}
            proveedoresList={proveedorList.results}
            updateList={updateList}
          />
        </>
      </WhiteSectionsPage>
    </>
  );
};
