import { Title } from '../../../../shared/text/title';
import { useParams } from 'react-router';
import { CrearCompraFormContainer } from '../componentes/crearCompraForm/crearCompraFormContainer';
import { WhiteSectionsPage } from '../../../../shared/containers/whiteSectionsPage';

export const ComprasNewEdit = () => {
  let params = useParams();

  return (
    <>
      <Title text={`${params.id ? 'Compra' : 'Nueva Compra'} `} />
      <div className="mx-[5%] my-10 rounded-md bg-white">
        <>
          <div className="rounded-md bg-white px-10 py-5">
            <CrearCompraFormContainer />
          </div>
        </>
      </div>
    </>
  );
};
