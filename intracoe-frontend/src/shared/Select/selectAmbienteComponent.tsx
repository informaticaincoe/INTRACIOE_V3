import { Dropdown } from 'primereact/dropdown';
import './selectCustomStyle.css';

interface SelectAmbienteProps {
  ambiente: any;
  setSelectAmbiente: any;
}

export const SelectAmbienteComponent: React.FC<SelectAmbienteProps> = ({
  ambiente,
  setSelectAmbiente,
}) => {
  // const [selectedAmbiente, setSelectedAmbiente] = useState(null);
  const cities = [
    { name: 'Modo producción', code: '1' },
    { name: 'Modo prueba', code: '2' },
  ];

  return (
    <div className="justify-content-center flex">
      <Dropdown
        value={ambiente} // El valor seleccionado se pasa desde el componente superior
        onChange={(e) => setSelectAmbiente(e.value)} // Al seleccionar un valor, se actualiza el estado en el componente superior
        options={cities}
        optionLabel="name"
        placeholder="Seleccionar ambiente"
        className="md:w-14rem font-display w-full"
      />
    </div>
  );
};
