import * as XLSX from 'xlsx';
import { WhiteSectionsPage } from '../../../../../shared/containers/whiteSectionsPage';
import { read, utils } from 'xlsx';

//icons
import { LuUpload } from 'react-icons/lu';
import { useState } from 'react';
import { createActivity } from '../../services/activitiesServices';
import { ActivitiesDataNew } from '../../../../../shared/interfaces/interfaces';

export const UploadFileSection = () => {
  const [excelData, setExcelData] = useState<ActivitiesDataNew[]>([]);
  //   const reader = new FileReader();
  //   reader.onload = (e: ProgressEvent<FileReader>) => {
  //     const ab = e.target?.result;
  //     if (ab) {
  //       const wb = XLSX.read(ab, { type: 'array' });
  //       const ws = wb.Sheets[wb.SheetNames[0]];
  //       const json: any[] = XLSX.utils.sheet_to_json(ws);
  //     }
  //   };
  //   reader.readAsArrayBuffer(file);
  // };

  // return (
  //   <WhiteSectionsPage>
  //     <article className="flex flex-col gap-10">
  //       <input
  //         type="file"
  //         accept=".xlsx,.xls,.csv"
  //         onChange={(e) => e.target.files && readExcel(e.target.files[0])}
  //         className="w-full self-start rounded-md"
  //       />
  //       <button
  //         type="button"
  //         className="flex items-center gap-5 self-start rounded-md border px-18 py-2"
  //       >
  //         <LuUpload />
  //         Subir
  //       </button>
  //     </article>
  //   </WhiteSectionsPage>
  // );

  const handleFileUpload = (e: any) => {
    const file = e.target.files[0];
    const reader = new FileReader();

    reader.onload = (e) => {
      const ab = e.target?.result;
      if (ab) {
        const wb = read(ab, { type: 'array' }); // Leer el archivo como un array
        const ws = wb.Sheets[wb.SheetNames[0]]; // Obtener la primera hoja
        const data = utils.sheet_to_json(ws, { header: 1 }); // Usamos { header: 1 } para que devuelva un array de arrays

        processExcelData(data); // Procesamos los datos
      }
    };

    reader.readAsArrayBuffer(file);
  };

  const processExcelData = (data: any[]) => {
    // Filtramos y mapeamos solo las filas que tienen datos en la primera columna y que el código es un número
    const extractedData = data
      .filter((row) => {
        const codigo = row[0];
        // Verificamos si el código no está vacío y si el código es un número
        return codigo && !isNaN(Number(codigo)); // El código debe ser numérico
      })
      .map((row) => ({
        codigo: row[0], // columna 1 que contine el codigo de las actividades
        descripcion: row[1], // columna 2 que contine el codigo de las actividades
      }));

    console.log(extractedData); // Ver los datos procesados
    setExcelData(extractedData); // Guardamos los datos en el estado
  };

  const handleUpload = async () => {
    try {
      excelData.map((data) => {
        createActivity(data);
      });
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <WhiteSectionsPage>
      <article className="flex flex-col gap-10">
        <input
          type="file"
          className="w-full self-start rounded-md"
          onChange={handleFileUpload}
        />
        <button
          type="button"
          className="flex items-center gap-5 self-start rounded-md border px-18 py-2"
          onClick={handleUpload}
        >
          <LuUpload />
          Subir
        </button>
      </article>
    </WhiteSectionsPage>
  );
};
