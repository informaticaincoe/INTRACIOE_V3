import * as XLSX from 'xlsx';
import { WhiteSectionsPage } from '../../../../../shared/containers/whiteSectionsPage';

//icons
import { LuUpload } from "react-icons/lu";

export const UploadFileSection = () => {
    const readExcel = (file: File) => {
        const reader = new FileReader();
        reader.onload = (e: ProgressEvent<FileReader>) => {
            const ab = e.target?.result;
            if (ab) {
                const wb = XLSX.read(ab, { type: 'array' });
                const ws = wb.Sheets[wb.SheetNames[0]];
                const json: any[] = XLSX.utils.sheet_to_json(ws);
                console.log(json); //mostrar la conversion a json en consola
            }
        };
        reader.readAsArrayBuffer(file);
    };
    return (
        <WhiteSectionsPage>
            <article className='flex flex-col gap-10'>
                <input
                    type="file"
                    accept=".xlsx,.xls,.csv"
                    onChange={(e) => e.target.files && readExcel(e.target.files[0])}
                    className='self-start w-full rounded-md'
                />
                <button type="button" className='flex items-center gap-5 border rounded-md px-18 py-2 self-start'><LuUpload />Subir</button>
            </article>
        </WhiteSectionsPage>
    )
}