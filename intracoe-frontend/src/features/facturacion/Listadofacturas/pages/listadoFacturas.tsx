import { useEffect, useState } from 'react';
import { WhiteSectionsPage } from '../../../../shared/containers/whiteSectionsPage';
import { Title } from '../../../../shared/text/title';
import { TableListadoFacturasContainer } from '../componentes/TableListadoFacturasContainer';
import { ListResult } from '../../../../shared/interfaces/interfaceFacturaJSON';
import { getAllFacturas } from '../services/listadoFacturasServices';
import { FilterContainer } from '../componentes/filter/filterContainer';
import { pagination } from '../../../../shared/interfaces/interfaces';

export const ListadoFActuras = () => {
  const [data, setData] = useState<ListResult[]>([]);
  const [pagination, setPagination] = useState<pagination>({
    has_next: false,
    has_previous: false,
    page: 0,
    pages: 0,
    total: 0,
  });

  const [rows, setRows] = useState<number>(20); // Django lo maneja en 20 por defecto
  const [first, setFirst] = useState<number>(0);

  useEffect(() => {
    fetchFacturas();
  }, []);

  const fetchFacturas = async (page = 1, limit = 20) => {
    try {
      const response = await getAllFacturas({ page, limit }); // ← importante: acepta parámetros
      setData(response.facturas);
      setPagination(response.pagination);
    } catch (error) {
      console.log(error);
    }
  };

  const handlePageChange = (page: number, limit: number) => {
    fetchFacturas(page, limit);
  };


  return (
    <>
      <Title text="Listado Facturas" />
      <WhiteSectionsPage className="px-20 py-10">
        <>
          <FilterContainer total={pagination.total ?? 0} />
          <TableListadoFacturasContainer
            data={data}
            pagination={pagination}
            onPageChange={handlePageChange}
          />


        </>
      </WhiteSectionsPage>
    </>
  );
};
