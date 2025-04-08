import { useEffect, useState } from 'react'
import { ModalReceptor } from '../../../facturacion/generateDocuments/components/Shared/receptor/modalReceptor'
import { ReceptorInterface } from '../../../../shared/interfaces/interfaces';
import { getAllReceptor } from '../../../../shared/services/receptor/receptorServices';
import { FormReceptoresContainer } from '../components/form/formReceptoresContainer';

export const NuevoReceptorPage = () => {
 const [receptoresList, setReceptoreLists] = useState<ReceptorInterface[]>([]);

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

    return (
        <div>
          <h1>rrrrrrrrrrrrrrr</h1>
            <FormReceptoresContainer/>
        </div>
    )
}
