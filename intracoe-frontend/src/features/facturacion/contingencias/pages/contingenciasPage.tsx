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

  export const ContingenciasPage = () => {
    const [contingenciasList, setContingenciasList] = useState<Contingencias | null>(null);
    // const [tiposDte, setTiposDte] = useState<{ id: number; codigo: string; descripcion: string }[]>([]);
    const [expandedRows, setExpandedRows] = useState<any[]>([]);
    const [filters, setFilters] = useState<FilterContingencia>({
      recibido_mh: null,
      sello_recepcion: '',
      has_sello_recepcion: null,
      tipo_dte: null,
    });

    const [pagination, setPagination] = useState({
      currentPage: 1,
      totalRecords: 0,
      pageSize: 10,
      next: '' as string | null,
      previous: '' as string | null,
    });

    useEffect(() => {
      fetchContingencias(pagination.currentPage, filters);
    }, [pagination.currentPage]);


    useEffect(() => {
      setPagination(p => ({ ...p, currentPage: 1 }));
      fetchContingencias(1, filters);
    }, [filters])

    const fetchContingencias = async (page: number, filters: FilterContingencia) => {
      try {
        const response = await GetAlEventosContingencia(page, filters);
        if (response) {
          setContingenciasList(response);
          // setTiposDte(response.tipos_dte);
          setPagination(p => ({
            ...p,
            currentPage: page,
            totalRecords: response.count,
            next: response.next,
            previous: response.previous,
          }));
        }
      } catch (error) {
        console.error('Error al cargar contingencias:', error);
      }
    };
    const rowExpansionTemplate = (rowData: any) => {
      return (
        <div className="flex w-full flex-col justify-center px-10">
          <TablaLotes lotes={rowData.facturas_en_grupos} />
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
              setFilters={setFilters}
              filters={filters}
            />
            <TablaContainerContingencias
              contingenciasList={contingenciasList?.results}
              expandedRows={expandedRows}
              setExpandedRows={setExpandedRows}
              rowExpansionTemplate={rowExpansionTemplate}
              pagination={pagination} // Paginación añadida
              setPagination={setPagination} // Función para actualizar la paginación
            />
          </>
        </WhiteSectionsPage>
      </>
    );
  };
