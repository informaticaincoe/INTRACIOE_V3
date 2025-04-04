import { Dialog } from 'primereact/dialog';
import { Divider } from 'primereact/divider';
import { Dropdown } from 'primereact/dropdown';
import React, { useEffect, useState } from 'react';
import {
  getAllTipoTributos,
  getAllTributosByTipo,
} from '../../../../../../shared/services/tributos/tributos';
import { MultiSelect } from 'primereact/multiselect';
import {
  TipoTributos,
  Tributos,
} from '../../../../../../shared/interfaces/interfaces';

interface ModalAgregarTibutoInterface {
  onClick?: (event: React.MouseEvent<HTMLButtonElement>) => void;
  visible: boolean;
  setVisible: any;
}

export const ModalAgregarTributo: React.FC<ModalAgregarTibutoInterface> = ({
  onClick,
  visible,
  setVisible,
}) => {
  const [tipoTributo, setTipoTributo] = useState<TipoTributos[]>([]);
  const [selectedTipoTributo, setSelectedTipoTributo] =
    useState<TipoTributos>();

  const [tributos, setTributos] = useState<Tributos[]>([]);
  const [selectedTributos, setSelectedTributos] = useState<Tributos[]>([]);

  useEffect(() => {
    fetchTipoTributos();
  }, []);

  useEffect(() => {
    fetchTributosSegunTipo();
  }, [selectedTipoTributo]);

  const fetchTipoTributos = async () => {
    try {
      const tipoTributosData = await getAllTipoTributos();
      setTipoTributo(tipoTributosData);
    } catch (error) {
      console.log(error);
    }
  };

  const fetchTributosSegunTipo = async () => {
    if (selectedTipoTributo) {
      try {
        const tipoTributosData = await getAllTributosByTipo(
          selectedTipoTributo.id
        );
        setTributos(tipoTributosData);
      } catch (error) {
        console.log(error);
      }
    }
  };

  return (
    <div className="justify-content-center flex">
      <Dialog
        header="Agregar tributos"
        visible={visible}
        style={{ width: '50%' }}
        onHide={() => {
          if (!visible) return;
          setVisible(false);
        }}
      >
        <div className="flex flex-col gap-5">
          <div className="flex flex-col gap-2">
            <>
              <label htmlFor="VentaTerceros">Tipo tributos</label>
              <Dropdown
                value={selectedTipoTributo}
                onChange={(e) => setSelectedTipoTributo(e.value)}
                options={tipoTributo}
                optionLabel="descripcion"
                placeholder="Seleccionar tipo de tributo"
                className="md:w-14rem font-display w-full"
              />
            </>
            <>
              <label htmlFor="porcentajeRetencion">Tributo</label>
              <MultiSelect
                value={selectedTributos}
                onChange={(e) => setSelectedTributos(e.value)}
                options={tributos}
                optionLabel="descripcion"
                placeholder="Seleccionar tipo de tributo"
                className="md:w-14rem font-display w-full"
              />
            </>
          </div>
        </div>
        <Divider />

        <div>
          <h2 className="text-lg font-semibold">Tributos aplicados</h2>
          <ul className="list-inside list-disc px-4">
            {selectedTributos.map((tributo) => (
              <li>{tributo.descripcion}</li>
            ))}
          </ul>
        </div>

        <Divider />
        <span className="flex justify-between">
          <p>Total retencion: $0.00</p>
          <span className="flex justify-end gap-2">
            <button
              className="bg-primary-blue w-[8vw] rounded-md py-2 text-white hover:cursor-pointer"
              onClick={onClick}
            >
              Aplicar
            </button>
            <button
              className="border-grauy text-grauy w-[8vw] rounded-md border py-2 hover:cursor-pointer"
              onClick={() => setVisible(false)}
            >
              Cancelar
            </button>
          </span>
        </span>
      </Dialog>
    </div>
  );
};
