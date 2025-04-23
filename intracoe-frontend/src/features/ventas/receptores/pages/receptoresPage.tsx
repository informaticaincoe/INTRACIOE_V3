import { useEffect, useRef, useState } from 'react';
import { WhiteSectionsPage } from '../../../../shared/containers/whiteSectionsPage';
import { Title } from '../../../../shared/text/title';
import { Divider } from 'primereact/divider';
import { TableReceptores } from '../components/tableReceptores';
import {
  deleteReceptor,
  getAllReceptor,
} from '../../../../shared/services/receptor/receptorServices';
import { ReceptorInterface } from '../../../../shared/interfaces/interfaces';
import { HeaderReceptoresOptions } from '../components/headerReceptoresOptions';
import {
  CustomToastRef,
  ToastSeverity,
} from '../../../../shared/toast/customToast';
import { useNavigate } from 'react-router';

import { FaCheckCircle } from 'react-icons/fa';
import { IoMdCloseCircle } from 'react-icons/io';

export const ReceptoresPage = () => {
  const [receptores, setReceptores] = useState<ReceptorInterface[]>([]);
  const [codigoFiltro, setCodigoFiltro] = useState<string>('');
  const [selectedReceptores, setSelectedReceptores] = useState<any[]>([]);
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
    console.log('d');
  }, [codigoFiltro, setSelectedReceptores, selectedReceptores]);

  const fetchReceptores = async () => {
    try {
      const response = await getAllReceptor({
        filter: codigoFiltro || undefined,
      });
      console.log(response);
      setReceptores(response);
    } catch (error) {
      console.log(error);
    }
  };

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
            receptores={receptores}
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
