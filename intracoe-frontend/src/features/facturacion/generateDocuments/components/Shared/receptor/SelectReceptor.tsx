import { Dropdown } from 'primereact/dropdown';
import React, { useEffect, useRef, useState } from 'react';
import { Dialog } from 'primereact/dialog';
import { getAllReceptor } from '../../../../../../shared/services/receptor/receptorServices';
import { ReceptorInterface } from '../../../../../../shared/interfaces/interfaces';
import { ModalReceptor } from './modalReceptor';
import { FormReceptoresContainer } from '../../../../../ventas/receptores/components/form/formReceptoresContainer';
import { Toast } from 'primereact/toast';

interface StepperProps {
  receptor: ReceptorInterface;
  setReceptor: (receptor: ReceptorInterface) => void;
  errorReceptor: boolean;
  setErrorReceptor: any;
}

export const SelectReceptor: React.FC<StepperProps> = ({
  receptor,
  setReceptor,
  errorReceptor,
  setErrorReceptor,
}) => {
  const [receptoresList, setReceptoreLists] = useState<ReceptorInterface[]>([]);
  const [visibleModal, setVisibleModal] = useState(false);
  const [updateReceptores, setUpdateReceptores] = useState(false);
  const toast = useRef<Toast>(null);

  useEffect(() => {
    fetchReceptores();
  }, []);

  const handleModalSuccess = () => {
    toast.current?.show({
      severity: 'success',
      summary: 'Receptor creado',
      detail: 'Se ha guardado correctamente',
      life: 3000,
    });
    setVisibleModal(false);
    setUpdateReceptores((prev) => !prev);
  };

  useEffect(() => {
    fetchReceptores();
    setVisibleModal(false);
    console.log('dentro', visibleModal);
  }, [updateReceptores]);

  const fetchReceptores = async () => {
    try {
      const response = await getAllReceptor();
      setReceptoreLists(response);
    } catch (error) {
      console.log(error);
    }
  };

  const hadleChange = (value: any) => {
    setReceptor(value);
    if (errorReceptor) setErrorReceptor(!errorReceptor);
  };

  return (
    <>
      <div className="flex flex-col items-start gap-1">
        <label htmlFor={receptor.id} className="opacity-70">
          Receptor
        </label>
        <div className="flex w-full justify-between gap-10">
          <Dropdown
            id={receptor.id}
            value={receptor}
            onChange={(e: { value: any }) => {
              hadleChange(e.value);
            }}
            options={receptoresList}
            optionLabel="nombre"
            placeholder="Seleccione un receptor"
            className={`font-display w-full text-start ${errorReceptor ? 'p-invalid' : ''} `}
            filter
          />
          <button
            className="bg-primary-blue rounded-md px-5 py-2 text-nowrap text-white hover:cursor-pointer"
            onClick={() => setVisibleModal(true)}
          >
            Añadir nuevo receptor
          </button>
        </div>
        {errorReceptor && (
          <p className="text-red">Campo receptor no debe estar vacio</p>
        )}
      </div>

      <Toast ref={toast} />
      <Dialog
        visible={visibleModal}
        modal
        style={{ width: '60vw', margin: 0, padding: 0 }}
        onHide={() => {
          if (!visibleModal) return;
          setVisibleModal(false);
        }}
      >
        <FormReceptoresContainer
          className="mt-0 mr-0 mb-0 ml-0"
          onSuccess={handleModalSuccess}
        />
      </Dialog>
    </>
  );
};
