import { useEffect, useState } from 'react';
import {
  InputNumber,
  InputNumberValueChangeEvent,
} from 'primereact/inputnumber';
import { SendFormButton } from '../../../../../../../shared/buttons/sendFormButton';
import { DropDownTipoDte } from '../tipoDocumento/DropdownTipoDte';
import { Dialog } from 'primereact/dialog';
import { SelectTipoGeneracionDelDocumento } from './selectTipoGeneracionDelDocumento';

interface ButtonDocumentosRelacionadosInterface {
  visible: any;
  setVisible: any;
}

export const ButtonDocumentosRelacionados: React.FC<
  ButtonDocumentosRelacionadosInterface
> = ({ visible, setVisible }) => {
  const [tipoDTERelacionado, setTipoDTERelacionado] = useState<any>();
  const [tipoGeneracionDTE, setTipoGeneracionDTE] = useState<any>();
  const [guardarListAux, setGuardarListAux] = useState<any[]>([]);
  const [checked, setChecked] = useState<boolean>(false);

  const [formData, setFormData] = useState({
    tipoDocRelacionado: '',
    TipoGeneracionDocumento: 0,
    numDocRelacionado: 0,
  });

  const handleChange = (e: InputNumberValueChangeEvent) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const onClick = () => {
    formData.tipoDocRelacionado = tipoDTERelacionado.name;
    formData.TipoGeneracionDocumento = tipoGeneracionDTE;

    setGuardarListAux((prevState) => [...prevState, { ...formData }]);
    // limpiar formulario
    setFormData({
      tipoDocRelacionado: '',
      TipoGeneracionDocumento: 0,
      numDocRelacionado: 0,
    });
  };

  return (
    <div className="flex w-full flex-col items-start">
      <span className="flex gap-3 text-start">
        <SendFormButton
          onClick={() => setVisible(true)}
          text={'Relacionar documento'}
          className="bg-blue-yellow border-primary-blue text-primary-blue border px-5 text-nowrap"
        ></SendFormButton>
      </span>

      <Dialog
        visible={visible}
        onHide={() => {
          if (!visible) return;
          setVisible(false);
        }}
      >
        <div className="flex w-[100%] flex-col gap-5 rounded-md border border-gray-200 px-10 py-8">
          <div className="flex justify-between gap-5">
            {' '}
            {/* Formulario */}
            <span className="flex w-full flex-col gap-1">
              <label htmlFor="montoPagar" className="text-start opacity-70">
                Tipo de documento relacionado
              </label>
              <DropDownTipoDte
                tipoDocumento={tipoDTERelacionado}
                setTipoDocumento={setTipoDTERelacionado}
                setTipoDocumentoSelected={undefined}
                tipoDocumentoSelected={undefined}
              />
            </span>
            <span className="flex w-full flex-col gap-1">
              <label htmlFor="montoPagar" className="text-start opacity-70">
                Tipo de generacion del documento
              </label>
              <SelectTipoGeneracionDelDocumento
                tipoGeneracion={tipoGeneracionDTE}
                setTipoGeneracion={setTipoGeneracionDTE}
              />
            </span>
            <span className="flex w-full flex-col gap-1">
              <label
                htmlFor="numDocRelacionado"
                className="text-start opacity-70"
              >
                Número de documento relacionado
              </label>
              <InputNumber
                name="numDocRelacionado"
                inputId="numDocRelacionado"
                placeholder="Número de documento"
                useGrouping={false}
                value={formData.numDocRelacionado}
                onValueChange={(e: InputNumberValueChangeEvent) =>
                  handleChange(e)
                }
              />
            </span>
          </div>
          <span className="flex items-end justify-end gap-4">
            <SendFormButton
              className="border-primary-blue text-primary-blue w-30 border py-2"
              text="Limpiar"
              onClick={() => {}}
            />
            <SendFormButton
              className="bg-primary-blue w-30 py-2 text-white"
              text="Relacionar"
              onClick={() => setVisible(!visible)}
            />
          </span>
        </div>
      </Dialog>
    </div>
  );
};
