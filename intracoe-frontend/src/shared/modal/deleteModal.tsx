import { useEffect, useRef } from 'react';
import { ConfirmDialog, confirmDialog } from 'primereact/confirmdialog';
import { Toast } from 'primereact/toast';
import { ActivitiesData } from '../../features/facturacion/activities/interfaces/activitiesData';
import styles from './modalCustom.module.css';

interface DeleteModalProps {
  activity: ActivitiesData;
  onClose: () => void; // Función para cerrar el modal
}

export const DeleteModal: React.FC<DeleteModalProps> = ({
  activity,
  onClose,
}) => {
  const toast = useRef<Toast | null>(null);

  const accept = () => {
    if (toast.current) {
      toast.current.show({
        severity: 'info',
        summary: 'Confirmed',
        detail: 'Activity deleted',
        life: 3000,
      });
    }
    onClose();
  };

  const reject = () => {
    if (toast.current) {
      toast.current.show({
        severity: 'warn',
        summary: 'Rejected',
        detail: 'You have rejected',
        life: 3000,
      });
    }
    onClose();
  };

  const showTemplate = () => {
    confirmDialog({
      group: 'templating',
      header: <p className="text-2xl">Eliminar actividad económica</p>,
      message: (
        <div className="flex-column align-items-center border-bottom-1 surface-border flex w-full">
          <span>
            ¿Estas seguro que deseas eliminar la actividad economica:{' '}
            <span className="italic">"{activity.descripcion}"</span>?
          </span>
        </div>
      ),
      accept,
      reject,
    });
  };

  useEffect(() => {
    if (activity) {
      showTemplate();
    }
  }, [activity]);

  return (
    <>
      <Toast ref={toast} />
      <ConfirmDialog
        group="templating"
        acceptLabel={'Eliminar'}
        rejectLabel="Cancelar"
        acceptClassName={styles.delete}
        rejectClassName={styles.cancel}
      />
    </>
  );
};
