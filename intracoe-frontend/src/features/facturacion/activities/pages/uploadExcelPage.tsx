import { Title } from '../../../../shared/text/title';
import { UploadFileSection } from '../components/uploadExcel/uploadFileSection';

export const UploadExcelPage = () => {
  return (
    <div>
      <Title text="Cargar actividades económicas" />
      <UploadFileSection />
    </div>
  );
};
