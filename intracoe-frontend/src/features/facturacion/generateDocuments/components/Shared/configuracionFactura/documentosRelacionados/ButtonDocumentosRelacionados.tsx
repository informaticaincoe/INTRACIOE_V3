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
  visible: any,
  setVisible: any
}

export const ButtonDocumentosRelacionados: React.FC<ButtonDocumentosRelacionadosInterface> = ({ visible, setVisible }) => {
  const [tipoDTERelacionado, setTipoDTERelacionado] = useState<any>();
  const [tipoGeneracionDTE, setTipoGeneracionDTE] = useState<any>();
  const [guardarListAux, setGuardarListAux] = useState<any[]>([]);
  const [checked, setChecked] = useState<boolean>(false);

  const [formData, setFormData] = useState({
    tipoDocRelacionado: '',
    TipoGeneracionDocumento: 0,
    numDocRelacionado: 0,
  });

  useEffect(() => {
    console.log("#");
    console.log(checked);
  }, [checked]);


  useEffect(() => {
    console.log(tipoGeneracionDTE);
  }, [tipoGeneracionDTE]);

  const handleChange = (e: InputNumberValueChangeEvent) => {
    console.log(e.target.name, e.target.value);
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const onClick = () => {
    formData.tipoDocRelacionado = tipoDTERelacionado.name
    formData.TipoGeneracionDocumento = tipoGeneracionDTE

    console.log(formData)

    setGuardarListAux((prevState) => [
      ...prevState, { ...formData },
    ]);
    // limpiar formulario
    setFormData({ tipoDocRelacionado: '', TipoGeneracionDocumento: 0, numDocRelacionado: 0 });
  };

  return (
    <div className="flex w-full flex-col items-start">
      <span className="flex gap-3 text-start">
        <SendFormButton
          onClick={( ) => setVisible(true)} text={'Relacionar documento'} className="text-nowrap bg-blue-yellow border-primary-blue border px-5 text-primary-blue"></SendFormButton>
      </span>

      <Dialog visible={visible} onHide={() => { if (!visible) return; setVisible(false); }} >
          <div className="flex w-[100%] flex-col gap-5 rounded-md border border-gray-200 px-10 py-8">
            <div className="flex gap-5 justify-between "> {/* Formulario */}
              <span className='flex flex-col gap-1 w-full'>
                <label htmlFor="montoPagar" className="text-start opacity-70">
                  Tipo de documento relacionado
                </label>
                <DropDownTipoDte tipoDocumento={tipoDTERelacionado} setTipoDocumento={setTipoDTERelacionado} />
              </span>
              <span className='flex flex-col gap-1 w-full'>
                <label htmlFor="montoPagar" className="text-start opacity-70">
                  Tipo de generacion del documento
                </label>
                <SelectTipoGeneracionDelDocumento tipoGeneracion={tipoGeneracionDTE} setTipoGeneracion={setTipoGeneracionDTE} />
              </span>
              <span className='flex flex-col gap-1 w-full'>
                <label htmlFor="numDocRelacionado" className="text-start opacity-70">
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
            <span className='flex gap-4 justify-end items-end'>
              <SendFormButton className='w-30 border border-primary-blue text-primary-blue py-2' text="Limpiar" onClick={() => { }} />
              <SendFormButton className='w-30 bg-primary-blue text-white py-2' text="Relacionar" onClick={() => setVisible(!visible)} />
            </span>
          </div>
      </Dialog>
    </div>
  );
};
