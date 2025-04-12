import { InputText } from 'primereact/inputtext';
import { IoIosAdd } from 'react-icons/io';
import { RiFileExcel2Fill } from 'react-icons/ri';
import { Divider } from 'primereact/divider';
import { useNavigate } from 'react-router';
import { useState } from 'react';
import { IconButton } from '../../../../shared/buttons/iconButton';

interface HeaderTableProps {
    nombre: string
    setActivities: React.Dispatch<React.SetStateAction<any[]>>;
    filterTerm: string;
    setFilterTerm: (term: string) => void;
}

export const HeaderTable: React.FC<HeaderTableProps> = ({
    nombre,
    setActivities,
    filterTerm,
    setFilterTerm
}) => {
    const navigate = useNavigate();
    const [showModal, setShowModal] = useState(false);

    const handleNewActivity = () => {
        setShowModal(true);
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
                                setFilterTerm(e.target.value)
                            }}
                            className="w-full"
                        />
                    </div>

                    <article className="flex gap-2">
                        <IconButton
                            text="Nueva actividad"
                            icon={<IoIosAdd size={20} />}
                            className="bg-primary-blue hover:bg-primary-blue-hover"
                            onClick={handleNewActivity}
                        />
                        <IconButton
                            text="Cargar desde excel"
                            icon={<RiFileExcel2Fill size={20} />}
                            className="bg-green hover:bg-green-hover"
                            onClick={handleUploadExcel}
                        />
                    </article>
                </article>
                <Divider />
            </div>

            {/* {showModal && (
                <NewActivityForm
                    visible={showModal}
                    setVisible={setShowModal}
                />
            )} */}
        </>
    );
};
