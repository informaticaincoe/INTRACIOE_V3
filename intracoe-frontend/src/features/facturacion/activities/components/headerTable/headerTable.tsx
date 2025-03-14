import { IconButton } from '../../../../../shared/buttons/iconButton';
import { Divider } from 'primereact/divider';
import { useState } from 'react';

//iconss
import { IoIosAdd } from 'react-icons/io';
import { RiFileExcel2Fill } from 'react-icons/ri';
import { NewActivityForm } from '../forms/newActivityform';
import { useNavigate } from 'react-router';

export const HeaderTable = ({ setActivities }: { setActivities: any }) => {
  const navigate = useNavigate();
  const [showModal, setShowModal] = useState(false);
  const [modalType, setModalType] = useState<'new' | 'excel' | null>(null);

  const handleNewActivity = (type: any) => {
    setShowModal(!showModal);
    setModalType(type);
  };

  const handleUploadExcel = () => {
    navigate('/uploadExcel');
  };

  return (
    <>
      <div>
        <article className="flex items-center justify-between">
          <p className="px-5 text-lg font-bold">Lista</p>
          <article className="flex gap-2">
            <IconButton
              text="Nueva actividad"
              icon={<IoIosAdd size={20} />}
              className="bg-primary-blue hover:bg-primary-blue-hover"
              onClick={() => {
                handleNewActivity('new');
              }}
            />
            <IconButton
              text="Cargar desde excel"
              icon={<RiFileExcel2Fill size={20} />}
              className="bg-green hover:bg-green-hover"
              onClick={() => {
                handleUploadExcel();
              }}
            />
          </article>
        </article>
        <Divider />
      </div>
      {showModal && modalType == 'new' && (
        <NewActivityForm visible={showModal} setVisible={setShowModal} />
      )}
    </>
  );
};
