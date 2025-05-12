import React, { useEffect, useState } from 'react';
import { Title } from '../../../../shared/text/title';
import { WhiteSectionsPage } from '../../../../shared/containers/whiteSectionsPage';
import { Divider } from 'primereact/divider';
import { CompraInterface } from '../interfaces/comprasInterfaces';
import { TablaComprasHeader } from '../componentes/tablaComprasHeader';
import { TablaCompras } from '../componentes/tablaCompras';
import { getAllCompras } from '../services/comprasServices';
import { useSearchParams } from 'react-router';
import { Pagination } from '../../../../shared/interfaces/interfacesPagination';

export const ComprasPage = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const [loading, setLoading] = useState(false);
  const [comprasList, setComprasList] = useState<CompraInterface>({
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
    fetchCompras();
  }, []);

  useEffect(() => {
    // Reinicia a la página 1 cada vez que los filtros cambian
    setPagination((prev) => ({ ...prev, current_page: 1 }));
    // Se utiliza el page_size actual para la consulta
    fetchCompras(1, pagination.page_size); //enviar el numero de pagina actual 1 por defecto, enviar la cantidad de elementos en pagina
  }, []);

  const updateCompras = () => {
    fetchCompras(pagination.current_page);
  };

  const onPageChange = (event: any) => {
    const page = event.page + 1;
    const limit = event.rows;
    fetchCompras(page, limit);
  };

  const fetchCompras = async (page = 1, limit = 10) => {
    try {
      setLoading(true);
      const response = await getAllCompras({ page, limit });
      if (response) {
        setComprasList(response);
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

  const handleSearch = (nuevoCodigo: string) => {
    setCodigoFiltro(nuevoCodigo.trim());
  };
  return (
    <>
      <Title text={'Compras'} />

      <WhiteSectionsPage>
        <>
          <TablaComprasHeader codigo={codigoFiltro} onSearch={handleSearch} />
          <Divider />
          <TablaCompras
            pagination={pagination}
            onPageChange={onPageChange}
            comprasList={comprasList.results}
            updateList={updateCompras}
          />
        </>
      </WhiteSectionsPage>
    </>
  );
};
