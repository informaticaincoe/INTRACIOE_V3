import { WhiteSectionsPage } from '../../../../shared/containers/whiteSectionsPage';
import { Title } from '../../../../shared/text/title';
import { TablaContainerProductos } from '../componentes/tablaContainerProductos';

import { Divider } from 'primereact/divider';
import { TablaProductosHeader } from '../componentes/tablaProductosHeader';
import { useEffect, useState } from 'react';
import { ProductoResponse } from '../../../../shared/interfaces/interfaces';
import { getAllProducts } from '../../../../shared/services/productos/productosServices';
import { useSearchParams } from 'react-router';
import { ProductosInterface } from '../interfaces/productosInterfaces';
import { Pagination } from '../../../../shared/interfaces/interfacesPagination';

export const ProductsPage = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const [loading, setLoading] = useState(false);
  const [productos, setProductos] = useState<ProductosInterface>({
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

  // Cada vez que cambie el filtro, recargamos los productos
  useEffect(() => {
    fetchProductos();
  }, [codigoFiltro]);

  useEffect(() => {
    // Reinicia a la página 1 cada vez que los filtros cambian
    setPagination((prev) => ({ ...prev, current_page: 1 }));
    // Se utiliza el page_size actual para la consulta
    fetchProductos(1, pagination.page_size); //enviar el numero de pagina actual 1 por defecto, enviar la cantidad de elementos en pagina
  }, []);

  const updateDevolucionCompras = () => {
    fetchProductos(pagination.current_page);
  };

  const onPageChange = (event: any) => {
    const page = event.page + 1;
    const limit = event.rows;
    fetchProductos(page, limit);
  };

  const fetchProductos = async (page = 1, limit = 10) => {
    try {
      // Pasamos tipo=1 (productos) y, si hay código, también filter
      const response = await getAllProducts({
        page,
        limit,
        tipo: 1,
        filter: codigoFiltro || undefined,
      });
      if (response) {
        setProductos(response);
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

  // Handler que pasamos al header para que active la búsqueda
  const handleSearch = (nuevoCodigo: string) => {
    setCodigoFiltro(nuevoCodigo.trim());
  };

  return (
    <>
      <Title text="productos" />
      <WhiteSectionsPage>
        <div>
          <TablaProductosHeader codigo={codigoFiltro} onSearch={handleSearch} />
          <Divider />
          <TablaContainerProductos
            productos={productos.results}
            pagination={pagination}
            onPageChange={onPageChange}
            updateList={updateDevolucionCompras}
          />
        </div>
      </WhiteSectionsPage>
    </>
  );
};
