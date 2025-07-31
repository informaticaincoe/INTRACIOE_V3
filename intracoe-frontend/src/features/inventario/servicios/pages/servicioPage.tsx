import React, { useEffect, useState } from 'react';
import { Title } from '../../../../shared/text/title';
import { WhiteSectionsPage } from '../../../../shared/containers/whiteSectionsPage';
import { Divider } from 'antd';
import { TablaServiciosHeader } from '../componenetes/tablaServiciosHeader';
import { TablaContainerServicios } from '../componenetes/tablaContainerServicios';
import { getAllProducts } from '../../../../shared/services/productos/productosServices';
import { useSearchParams } from 'react-router';
import { ProductosInterface } from '../../products/interfaces/productosInterfaces';
import { Pagination } from '../../../../shared/interfaces/interfacesPagination';
import LoadingScreen from '../../../../shared/loading/loadingScreen';

export const ServicioPage = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const [loading, setLoading] = useState(false);
  const [servicios, setServicios] = useState<ProductosInterface>({
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

  // Cada vez que cambie el filtro, recargamos los servicios
  useEffect(() => {
    fetchServicios();
  }, [codigoFiltro]);

  useEffect(() => {
    // Reinicia a la página 1 cada vez que los filtros cambian
    setPagination((prev) => ({ ...prev, current_page: 1 }));
    // Se utiliza el page_size actual para la consulta
    fetchServicios(1, pagination.page_size); //enviar el numero de pagina actual 1 por defecto, enviar la cantidad de elementos en pagina
  }, []);

  const updateDevolucionCompras = () => {
    fetchServicios(pagination.current_page);
  };

  const onPageChange = (event: any) => {
    const page = event.page + 1;
    const limit = event.rows;
    fetchServicios(page, limit);
  };

  const fetchServicios = async (page = 1, limit = 10) => {
    try {
      setLoading(true);
      const response = await getAllProducts({
        page,
        limit,
        tipo: 2, // id servicio
        filter: codigoFiltro || undefined,
      });
      if (response) {
        setServicios(response);
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
  // Handler que pasamos al header para que active la búsqueda
  const handleSearch = (nuevoCodigo: string) => {
    setCodigoFiltro(nuevoCodigo.trim());
  };

  return (
    <>
      {loading && <LoadingScreen />}
      <Title text="Servicios" />
      <WhiteSectionsPage>
        <div>
          <TablaServiciosHeader codigo={codigoFiltro} onSearch={handleSearch} />
          <Divider />
          <TablaContainerServicios
            servicios={servicios.results}
            pagination={pagination}
            onPageChange={onPageChange}
            updateList={updateDevolucionCompras}
          />
        </div>
      </WhiteSectionsPage>
    </>
  );
};
