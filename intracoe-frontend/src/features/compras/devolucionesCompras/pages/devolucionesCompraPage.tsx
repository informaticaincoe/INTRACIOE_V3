import { useEffect, useState } from 'react';
import { Title } from '../../../../shared/text/title';
import { WhiteSectionsPage } from '../../../../shared/containers/whiteSectionsPage';
import { TablaDevolucionesCompra } from '../componentes/tablaDevolucionesCompra';
import { getAllDevolucionesCompra } from '../services/devolucionesCompraServices';
import { Pagination } from '../../../../shared/interfaces/interfacesPagination';
import { useSearchParams } from 'react-router';
import { DevolucionCompra } from '../interfaces/devolucionCompraInterfaces';
import LoadingScreen from '../../../../shared/loading/loadingScreen';

export const DevolucionesCompraPage = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const [loading, setLoading] = useState(false);
  const [devolucionesCompra, setDevolucionesCompra] =
    useState<DevolucionCompra>({
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

  useEffect(() => {
    fetchDevolucionesCompra();
  }, []);

  useEffect(() => {
    // Reinicia a la página 1 cada vez que los filtros cambian
    setPagination((prev) => ({ ...prev, current_page: 1 }));
    // Se utiliza el page_size actual para la consulta
    fetchDevolucionesCompra(1, pagination.page_size); //enviar el numero de pagina actual 1 por defecto, enviar la cantidad de elementos en pagina
  }, []);

  const updateDevolucionCompras = () => {
    fetchDevolucionesCompra(pagination.current_page);
  };

  const onPageChange = (event: any) => {
    const page = event.page + 1;
    const limit = event.rows;
    fetchDevolucionesCompra(page, limit);
  };

  const fetchDevolucionesCompra = async (page = 1, limit = 10) => {
    try {
      setLoading(true);
      const response = await getAllDevolucionesCompra({ page, limit });

      if (response) {
        setDevolucionesCompra(response);
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
    finally {
      setLoading(false);
    }
  };



  return (
    <>
      {loading && <LoadingScreen />}
      <Title text={'Devoluciones compra'} />

      <WhiteSectionsPage>
        <>
          {/* <TablaComprasHeader codigo={codigoFiltro} onSearch={handleSearch} />
                    <Divider /> */}
          <TablaDevolucionesCompra
            pagination={pagination}
            onPageChange={onPageChange}
            devolucionesList={devolucionesCompra.results} //enviar solo la lista de elementos
            updateList={updateDevolucionCompras}
          />
        </>
      </WhiteSectionsPage>
    </>
  );
};
