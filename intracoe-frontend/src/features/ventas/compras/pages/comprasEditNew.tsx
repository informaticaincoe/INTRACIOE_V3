import CustomToast, { CustomToastRef, ToastSeverity } from '../../../../shared/toast/customToast'
import { Title } from '../../../../shared/text/title'
import { useParams } from 'react-router';
import { CrearCompraFormContainer } from '../componentes/crearCompraForm/crearCompraFormContainer';

export const ComprasNewEdit = () => {
    let params = useParams();

    return (
        <>
            <Title text={`${params.id ? 'Compra' : 'Nueva Compra'} `} />
            <div className='bg-white rounded-md  my-10 mx-[20%]'>
                <CrearCompraFormContainer />
            </div>
        </>
    )
}
