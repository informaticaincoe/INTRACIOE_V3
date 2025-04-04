import { Dropdown } from 'primereact/dropdown';
import React, { useEffect, useState } from 'react';
import { Dialog } from 'primereact/dialog';
import { getAllReceptor } from '../../../../../../shared/services/receptor/receptorServices';
import { ReceptorInterface } from '../../../../../../shared/interfaces/interfaces';
import { ModalReceptor } from './modalReceptor';

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

  useEffect(() => {
    fetchReceptores();
  }, []);

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
      <Dialog
        header={<p className="text-xl">Nuevo receptor</p>}
        visible={visibleModal}
        modal
        style={{ width: 'auto' }}
        onHide={() => {
          if (!visibleModal) return;
          setVisibleModal(false);
        }}
      >
        <ModalReceptor
          setReceptoreLists={setReceptoreLists}
          receptoresList={receptoresList}
        />
      </Dialog>
    </>
  );
};
