import React, { useEffect, useState } from 'react';
import { AjusteInventarioInterface } from '../interfaces/ajusteInventarioInterfaces';
import { getAllAjusteInventario } from '../services/ajusteInventarioServices';
import { Title } from '../../../../shared/text/title';
import { WhiteSectionsPage } from '../../../../shared/containers/whiteSectionsPage';
import { Divider } from 'antd';
import { TablaAjusteInventario } from '../componentes/tablaAjusteInventario';
import { TablaInventarioHeader } from '../componentes/tablaAjusteInventarioHeader';
import { useSearchParams } from 'react-router';
import { Pagination } from '../../../../shared/interfaces/interfacesPagination';
import LoadingScreen from '../../../../shared/loading/loadingScreen';
import axios from 'axios';

export const AjusteInventarioPage = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const [loading, setLoading] = useState(false);
  const [ajusteInventario, setAjusteInventario] =
    useState<AjusteInventarioInterface>({
      count: 1,
      current_page: 1,
      page_size: 10,
      has_next: true,
      has_previous: false,
      results: [],
    });
  const [pagination, setPagination] = useState<Pagination>({
    count: 1,
    current_page: 1,
    page_size: 10,
    has_next: true,
    has_previous: false,
  });

  const [codigoFiltro, setCodigoFiltro] = useState<string>('');

  useEffect(() => {
    const controller = new AbortController();
    fetchAjusteInventario(1, 10, controller.signal);

    return () => {
      controller.abort();
    };
  }, []);


  useEffect(() => {
    // Reinicia a la página 1 cada vez que los filtros cambian
    setPagination((prev) => ({ ...prev, current_page: 1 }));
    // Se utiliza el page_size actual para la consulta
    fetchAjusteInventario(1, pagination.page_size); //enviar el numero de pagina actual 1 por defecto, enviar la cantidad de elementos en pagina
  }, []);

  const updateDevolucionCompras = () => {
    fetchAjusteInventario(pagination.current_page);
  };

  const onPageChange = (event: any) => {
    const page = event.page + 1;
    const limit = event.rows;
    fetchAjusteInventario(page, limit);
  };

  const fetchAjusteInventario = async (page = 1, limit = 10, signal?: AbortSignal) => {
    try {
      setLoading(true);
      const response = await getAllAjusteInventario({ page, limit, signal });
      if (response) {
        setAjusteInventario(response);
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
    } catch (error: any) {
      if (axios.isCancel(error)) {
        console.log('Petición cancelada Ajuste Inventario');
      } else {
        console.log(error);
      }
    } finally {
      setLoading(false);
    }
  };


  const handleSearch = (nuevoCodigo: string) => {
    setCodigoFiltro(nuevoCodigo.trim());
  };

  return (
    <>
      {loading && <LoadingScreen />}
      <Title text={'Ajuste de movimiento de inventario'} />

      <WhiteSectionsPage>
        <>
          <TablaInventarioHeader
            results={ajusteInventario.results.length ?? 0}
            codigo={codigoFiltro}
            onSearch={handleSearch}
          />
          <Divider />
          <TablaAjusteInventario
            ajusteInventario={ajusteInventario.results} //enviar solo la lista de elementos
            pagination={pagination}
            onPageChange={onPageChange}
            updateList={updateDevolucionCompras}
          />
        </>
      </WhiteSectionsPage>
    </>
  );
};
