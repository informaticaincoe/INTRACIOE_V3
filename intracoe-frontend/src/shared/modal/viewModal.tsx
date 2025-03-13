import { useEffect, useRef } from 'react';
import { ActivitiesData } from '../../features/facturacion/activities/interfaces/activitiesData';
import { Toast } from 'primereact/toast';
import { ConfirmDialog, confirmDialog } from 'primereact/confirmdialog';
// import styles from "./modalCustom.module.css"

interface ViewModalProps {
  activity: ActivitiesData;
  onClose: () => void; // Función para cerrar el modal
}

export const ViewModal: React.FC<ViewModalProps> = ({ activity, onClose }) => {
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
      header: <p className="px-10 text-2xl">Detalle de actividad económica</p>,
      message: (
        <div className="flex-column align-items-center border-bottom-1 surface-border flex w-full">
          <table className="font-display text-md">
            <tbody>
              <tr>
                <td className="text-gray px-5 py-2">Codigo:</td>
                <td className="text-black">{activity.codigo}</td>
              </tr>
              <tr>
                <td className="text-gray px-5">Descripción:</td>
                <td className="text-black">{activity.descripcion}</td>
              </tr>
            </tbody>
          </table>
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
        acceptLabel={'Ok'}
        rejectLabel="Cancelar"
      />
    </>
  );
};
