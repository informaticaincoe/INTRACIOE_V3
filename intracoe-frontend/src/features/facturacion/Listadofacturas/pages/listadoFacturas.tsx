import { useEffect, useState } from 'react';
import { WhiteSectionsPage } from '../../../../shared/containers/whiteSectionsPage';
import { Title } from '../../../../shared/text/title';
import { TableListadoFacturasContainer } from '../componentes/TableListadoFacturasContainer';
import {
  Filters,
  ListResult,
} from '../../../../shared/interfaces/interfaceFacturaJSON';
import { getAllFacturas } from '../services/listadoFacturasServices';
import { OptionsContainer } from '../componentes/filter/optionsContainer';
import { pagination } from '../../../../shared/interfaces/interfaces';

export const ListadoFacturas = () => {
  const [data, setData] = useState<ListResult[]>([]);
  const [pagination, setPagination] = useState<pagination>({
    current_page: 1,
    page_size: 1,
    total_pages: 1,
    total_records: 1,
  });

  const [filters, setFilters] = useState<Filters>({
    recibido_mh: null,
    sello_recepcion: null,
    has_sello_recepcion: null,
    estado: null,
    tipo_dte: null,
    estado_invalidacion: null,
  });

  useEffect(() => {
    fetchFacturas();
  }, []);

  useEffect(() => {
    // Reinicia a la página 1 cada vez que los filtros cambian
    setPagination((prev) => ({ ...prev, current_page: 1 }));
    console.log(filters)
    // Se utiliza el page_size actual para la consulta
    fetchFacturas(1, pagination.page_size);
  }, [filters]);

  const fetchFacturas = async (page = 1, limit = 20) => {
    try {
      const response = await getAllFacturas({ page, limit, filters });
      if (response) {
        setData(response.results || []);
        setPagination({
          current_page: response.current_page || 1,
          page_size: response.page_size || limit,
          total_pages: response.total_pages || 1,
          total_records: response.total_records || 0,
        });
      } else {
        // En caso de response null, asigna valores por defecto o maneja el error
        setData([]);
        setPagination({
          current_page: 1,
          page_size: limit,
          total_pages: 1,
          total_records: 0,
        });
      }
    } catch (error) {
      console.log(error);
    }
  };

  const onPageChange = (event: any) => {
    const page = event.page + 1;
    const limit = event.rows;
    fetchFacturas(page, limit);
  };

  return (
    <>
      <Title text="Listado Facturas" />
      <WhiteSectionsPage className="px-20 py-10">
        <>
          <OptionsContainer
            total={pagination.total_records ?? 0}
            setFilters={setFilters}
            filters={filters}
          />
          <TableListadoFacturasContainer
            data={data}
            pagination={pagination}
            onPageChange={onPageChange}
          />
        </>
      </WhiteSectionsPage>
    </>
  );
};
