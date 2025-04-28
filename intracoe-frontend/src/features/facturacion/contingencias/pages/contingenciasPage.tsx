import { useEffect, useState } from 'react';
import { Title } from '../../../../shared/text/title';
import { GetAlEventosContingencia } from '../services/contingenciaService.';
import { WhiteSectionsPage } from '../../../../shared/containers/whiteSectionsPage';
import {
  Contingencias,
  FilterContingencia,
} from '../interfaces/contingenciaInterfaces';
import { OptionsContainer } from '../componentes/filter/optionsContainer';

import { TablaContainerContingencias } from '../interfaces/tablas/tablaContainerContingencias';
import { TablaLotes } from '../interfaces/tablas/tablaLotes';
import { useSearchParams } from 'react-router';

export const ContingenciasPage = () => {
  const [searchParams, setSearchParams] = useSearchParams();

  const initialFilters: FilterContingencia = {
    recibido_mh: searchParams.has('recibido_mh')
      ? searchParams.get('recibido_mh') === 'true'
      : null,
    sello_recepcion: searchParams.get('sello_recepcion') || '',
    has_sello_recepcion: searchParams.has('has_sello_recepcion')
      ? searchParams.get('has_sello_recepcion') === 'true'
      : null,
    tipo_dte: searchParams.has('tipo_dte')
      ? parseInt(searchParams.get('tipo_dte')!, 10)
      : null,
  };

  const [contingenciasList, setContingenciasList] = useState<Contingencias | null>(null);
  const [expandedRows, setExpandedRows] = useState<any[]>([]);
  const [filters, setFilters] = useState<FilterContingencia>(initialFilters);

  const [pagination, setPagination] = useState({
    currentPage: 1,
    totalRecords: 0,
    pageSize: 20,
    next: '' as string | null,
    previous: '' as string | null,
  });

  useEffect(() => {
    const page = searchParams.get('page')
      ? parseInt(searchParams.get('page')!, 10)
      : 1;

    const newFilters: FilterContingencia = {
      recibido_mh: searchParams.has('recibido_mh')
        ? searchParams.get('recibido_mh') === 'true'
        : null,
      sello_recepcion: searchParams.get('sello_recepcion') || '',
      has_sello_recepcion: searchParams.has('has_sello_recepcion')
        ? searchParams.get('has_sello_recepcion') === 'true'
        : null,
      tipo_dte: searchParams.has('tipo_dte')
        ? parseInt(searchParams.get('tipo_dte')!, 10)
        : null,
    };

    setFilters(newFilters);
    setPagination(p => ({
      ...p,
      currentPage: page,
    }));

    fetchAllEventos(page, newFilters)
  }, [searchParams]);

  const fetchAllEventos = async (page: any, newFilters: any) => {
    await GetAlEventosContingencia(page, newFilters).then(response => {
      if (!response) return;
      setContingenciasList(response);
      setPagination(p => ({
        ...p,
        currentPage: page,
        totalRecords: response.count,
      }));
    });
  }

  const onFilterChange = (newFilters: FilterContingencia) => {
    // Reconstruyo params y reseteo la página a 1
    const params: Record<string, string> = { page: '1' };
    if (newFilters.recibido_mh !== null)
      params.recibido_mh = String(newFilters.recibido_mh);
    if (newFilters.sello_recepcion)
      params.sello_recepcion = newFilters.sello_recepcion;
    if (newFilters.has_sello_recepcion !== null)
      params.has_sello_recepcion = String(newFilters.has_sello_recepcion);
    if (newFilters.tipo_dte !== null)
      params.tipo_dte = String(newFilters.tipo_dte);

    setSearchParams(params);
  };

  // 4) Controlador para cambio de página desde la tabla:
  const onPageChange = (newPage: number) => {
    // Conservo los demás params (filtros)
    const params = Object.fromEntries(searchParams.entries());
    setSearchParams({ ...params, page: String(newPage) });
  };

  const updateContingencias = () => {
    fetchAllEventos(pagination.currentPage, filters);
  }

  const rowExpansionTemplate = (rowData: any) => {
    return (
      <div className="flex w-full flex-col justify-center px-10">
        <TablaLotes lotes={rowData.facturas_en_grupos} contingenciaEstado={rowData.recibido_mh} updateContingencias={updateContingencias}/>
      </div>
    );
  };

  return (
    <>
      <Title text="Listado de Facturas en Contiengencia" />
      <WhiteSectionsPage>
        <>
          <OptionsContainer
            total={contingenciasList?.count ?? 0}
            setFilters={onFilterChange}
            filters={filters}
          />
          <TablaContainerContingencias
            contingenciasList={contingenciasList?.results}
            expandedRows={expandedRows}
            setExpandedRows={setExpandedRows}
            rowExpansionTemplate={rowExpansionTemplate}
            pagination={pagination} // Paginación añadida
            setPagination={setPagination} // Función para actualizar la paginación
            onPageChange={onPageChange}
          />
        </>
      </WhiteSectionsPage>
    </>
  );
};
