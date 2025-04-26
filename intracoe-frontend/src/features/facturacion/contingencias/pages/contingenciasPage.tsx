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
  const [expandedRows, setExpandedRows] = useState<any[]>([]);
  const [filters, setFilters] = useState<FilterContingencia>({
    recibido_mh: null,
    sello_recepcion: null,
    has_sello_recepcion: null,
    tipo_dte: null,
  });

  const [pagination, setPagination] = useState({
    currentPage: 1,
    totalRecords: 0,
    pageSize: 10,
    next: '',
    previous: ''
  });

  useEffect(() => {
    fetchContingencias(1); // Llamamos a la API para cargar la primera página al inicio
  }, []);

  useEffect(() => {
    fetchContingencias(pagination.currentPage); // Llamamos a la API cada vez que cambia la página
  }, [pagination.currentPage]);

  const fetchContingencias = async (page: number) => {
    try {
      const response = await GetAlEventosContingencia(page); // Le pasas la página a la API
      if (response) {
        setContingenciasList(response);
        setPagination({
          currentPage: page, // La página actual es la que pasamos a la API
          pageSize: pagination.pageSize, // Se mantiene el tamaño de página
          totalRecords: response?.count ?? 0, // Total de registros en la API
          next: response?.next ?? '', // URL de la siguiente página
          previous: response?.previous ?? '', // URL de la página anterior
        });
      }
    } catch (error) {
      console.log(error);
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
