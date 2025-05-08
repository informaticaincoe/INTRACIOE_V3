import { useEffect, useRef, useState } from 'react';
import { WhiteSectionsPage } from '../../../../shared/containers/whiteSectionsPage';
import { Title } from '../../../../shared/text/title';
import { Divider } from 'primereact/divider';
import { TableReceptores } from '../components/tableReceptores';
import {
  deleteReceptor,
  getAllReceptor,
} from '../../../../shared/services/receptor/receptorServices';
import { HeaderReceptoresOptions } from '../components/headerReceptoresOptions';
import {
  CustomToastRef,
  ToastSeverity,
} from '../../../../shared/toast/customToast';
import { useNavigate, useSearchParams } from 'react-router';

import { FaCheckCircle } from 'react-icons/fa';
import { IoMdCloseCircle } from 'react-icons/io';
import { ReceptorInterface } from '../interfaces/receptorInterfaces';
import { Pagination } from '../../../../shared/interfaces/interfacesPagination';

export const ReceptoresPage = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const [loading, setLoading] = useState(false)
  const [receptores, setReceptores] = useState<ReceptorInterface>({
    count: 1,
    current_page: 1,
    page_size: 10,
    has_next: true,
    has_previous: false,
    results: []
  });
  const [codigoFiltro, setCodigoFiltro] = useState<string>('');
  const [selectedReceptores, setSelectedReceptores] = useState<any[]>([]);
  const [pagination, setPagination] = useState<Pagination>({
    count: 1,
    current_page: 1,
    page_size: 10,
    has_next: true,
    has_previous: false,
  });
  const toastRef = useRef<CustomToastRef>(null);
  const navigate = useNavigate();

  const handleAccion = (
    severity: ToastSeverity,
    icon: any,
    summary: string
  ) => {
    toastRef.current?.show({
      severity: severity,
      summary: summary,
      icon: icon,
      life: 2000,
    });
  };

  // Cada vez que cambie el filtro, recargamos los productos
  useEffect(() => {
    fetchReceptores();
  }, [codigoFiltro, setSelectedReceptores, selectedReceptores]);

  useEffect(() => {
    // Reinicia a la página 1 cada vez que los filtros cambian
    setPagination((prev) => ({ ...prev, current_page: 1 }));
    // Se utiliza el page_size actual para la consulta
    fetchReceptores(1, pagination.page_size); //enviar el numero de pagina actual 1 por defecto, enviar la cantidad de elementos en pagina
  }, []);

  const updateReceptores = () => {
    fetchReceptores(pagination.current_page);
  };

  const onPageChange = (event: any) => {
    const page = event.page + 1;
    const limit = event.rows;
    fetchReceptores(page, limit);
  };


  const fetchReceptores = async (page = 1, limit = 10) => {
    try {
      setLoading(true)
      const response = await getAllReceptor({
        filter: codigoFiltro || undefined, page, limit
      });
      if (response) {
        setReceptores(response)
        setPagination({
          count: response.count || 0,
          current_page: response.current_page || 1,
          page_size: response.page_size || limit,
          has_next: response.has_next,
          has_previous: response.has_previous
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
      console.log(error)
    }
  }

  const handleSearch = (nuevoCodigo: string) => {
    setCodigoFiltro(nuevoCodigo.trim());
  };

  const handleDelete = async () => {
    // Se itera sobre los productos seleccionados y se elimina uno por uno
    for (const receptor of selectedReceptores) {
      try {
        await deleteReceptor(receptor.id);
        handleAccion(
          'success',
          <FaCheckCircle size={38} />,
          'Receptor eliminado con éxito'
        );
        updateReceptores()
      } catch (error) {
        console.error(error);
        handleAccion(
          'error',
          <IoMdCloseCircle size={38} />,
          'Error al eliminar el receptor'
        );
      }
    }
    // Después de eliminar, se limpia la selección y se actualiza la lista de productos
    setSelectedReceptores([]);
  };

  const editHandler = () => {
    navigate(`/receptor/${selectedReceptores[0].id}`);
  };

  return (
    <>
      <Title text="Receptores" />
      <WhiteSectionsPage>
        <div>
          <HeaderReceptoresOptions
            codigo={codigoFiltro}
            onSearch={handleSearch}
          />
          <Divider />
          <TableReceptores
            pagination={pagination}
            onPageChange={onPageChange}
            updateList={updateReceptores}
            receptores={receptores.results}
            setSelectedReceptores={setSelectedReceptores}
            selectedReceptores={selectedReceptores}
            onDelete={handleDelete}
            onEdit={editHandler}
          />
        </div>
      </WhiteSectionsPage>
    </>
  );
};
