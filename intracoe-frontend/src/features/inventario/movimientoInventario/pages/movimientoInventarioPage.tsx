import { useEffect, useState } from 'react';
import { getAllMovimientosInventario } from '../services/movimientoInventarioServices';
import { movimientoInterface } from '../interfaces/movimientoInvetarioInterface';
import { WhiteSectionsPage } from '../../../../shared/containers/whiteSectionsPage';
import { Title } from '../../../../shared/text/title';
import { TablaInventarioHeader } from '../componentes/tablaInventarioHeader';
import { Divider } from 'primereact/divider';
import { TablaMovimientoInventario } from '../componentes/tablaMovimientoInventario';
import LoadingScreen from '../../../../shared/loading/loadingScreen';
import { Pagination } from '../../../../shared/interfaces/interfacesPagination';
import { useSearchParams } from 'react-router';

export const MovimientoInventarioPage = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const [movimientoList, setMovimientoList] = useState<movimientoInterface>({
    count: 1,
    current_page: 1,
    page_size: 10,
    has_next: true,
    has_previous: false,
    results: [],
  });
  const [codigoFiltro, setCodigoFiltro] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [pagination, setPagination] = useState<Pagination>({
    count: 1,
    current_page: 1,
    page_size: 10,
    has_next: true,
    has_previous: false,
  });

  useEffect(() => {
  const controller = new AbortController();
  fetchMovimientosInventario(1, 10, controller.signal);

  return () => controller.abort();
  }, []);

  useEffect(() => {
    // Reinicia a la página 1 cada vez que los filtros cambian
    setPagination((prev) => ({ ...prev, current_page: 1 }));
    // Se utiliza el page_size actual para la consulta
    fetchMovimientosInventario(1, pagination.page_size); //enviar el numero de pagina actual 1 por defecto, enviar la cantidad de elementos en pagina
  }, []);

  const updateMovimientos = () => {
    fetchMovimientosInventario(pagination.current_page);
  };

  const onPageChange = (event: any) => {
    const page = event.page + 1;
    const limit = event.rows;
    fetchMovimientosInventario(page, limit);
  };

  const fetchMovimientosInventario = async (page = 1, limit = 10, signal?: AbortSignal) => {
    try {
      setLoading(true);
      const response = await getAllMovimientosInventario({ page, limit }, signal);
      if (response) {
        setMovimientoList(response);
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
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (nuevoCodigo: string) =>
    setCodigoFiltro(nuevoCodigo.trim());

  return (
    <>
      {loading && <LoadingScreen />}
      <Title text={'Movimiento de inventario'} />

      <WhiteSectionsPage>
        <>
          <TablaInventarioHeader
            results={pagination.count ?? 0}
            codigo={codigoFiltro}
            onSearch={handleSearch}
          />
          <Divider />
          <TablaMovimientoInventario
            pagination={pagination} //enviar datos de paginacion
            onPageChange={onPageChange} //funcion para cambiar de pagina
            movimientoList={movimientoList.results} //enviar solo los resultados
            updateMovimientos={updateMovimientos} //enviar funcion apra actualizar movimientos
          />
        </>
      </WhiteSectionsPage>
    </>
  );
};
