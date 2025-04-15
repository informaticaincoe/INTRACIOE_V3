import { InputText } from 'primereact/inputtext';
import { IoIosAdd } from 'react-icons/io';
import { RiFileExcel2Fill } from 'react-icons/ri';
import { Divider } from 'primereact/divider';
import { useNavigate } from 'react-router';
import { IconButton } from '../../../../shared/buttons/iconButton';
interface HeaderTableProps {
  nombre: string;
  filterTerm: string;
  setFilterTerm: (term: string) => void;
  setShowModalNew: any;
}

export const HeaderTable: React.FC<HeaderTableProps> = ({
  nombre,
  filterTerm,
  setFilterTerm,
  setShowModalNew,
}) => {
  const navigate = useNavigate();

  const handleNewActivity = () => {
    setShowModalNew(true);
  };

  const handleUploadExcel = () => {
    navigate('/uploadExcel');
  };

  return (
    <>
      <div>
        <article className="flex items-center justify-between">
          <p className="px-5 text-lg font-bold">{nombre}</p>

          {/*  INPUT DE FILTRO  */}
          <div className="flex-1 px-5">
            <InputText
              placeholder="Filtrar por código o descripción"
              value={filterTerm}
              onChange={(e) => {
                setFilterTerm(e.target.value);
              }}
              className="w-full"
            />
          </div>

          <article className="flex gap-2">
            <IconButton
              text="Añadir"
              icon={<IoIosAdd size={20} />}
              className="bg-primary-blue hover:bg-primary-blue-hover"
              onClick={handleNewActivity}
            />
            {nombre == 'Actividades economicas' && (
              <IconButton
                text="Cargar desde excel"
                icon={<RiFileExcel2Fill size={20} />}
                className="bg-green hover:bg-green-hover"
                onClick={handleUploadExcel}
              />
            )}
          </article>
        </article>
        <Divider />
      </div>
    </>
  );
};
