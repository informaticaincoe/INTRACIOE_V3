import React, { useEffect, useRef, useState } from 'react';
import { Accordion, AccordionTab } from 'primereact/accordion';
import { FaTruck } from 'react-icons/fa6';
import { FaFileAlt } from 'react-icons/fa';
import { OtrosDocumentosAsociados } from '../../../../../shared/interfaces/interfaces';
import { getOtrosDocumentosAsociadosById } from '../../../../../shared/catalogos/services/catalogosServices';
import { IoClose } from 'react-icons/io5';
import { Menu } from 'primereact/menu';
import { MdDelete } from 'react-icons/md';

interface Props {
  documentos: OtrosDocumentosAsociados[];
  setDocumentos: any;
}

const getIcon = (code: number) => {
  if (code === 4) return <FaTruck className="text-xl text-blue-600" />;
  return <FaFileAlt className="text-xl text-green-600" />;
};

const renderDetails = (doc: OtrosDocumentosAsociados) => {
  const fields = ['modoTransp', 'placaTrans', 'numConductor', 'nombreConductor', 'detalleDocumento'];
  const labels: Record<string, string> = {
    modoTransp: 'Modo de transporte',
    placaTrans: 'Placa',
    numConductor: 'Cédula conductor',
    nombreConductor: 'Nombre conductor',
    detalleDocumento: 'Descripción',
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 p-4 rounded">
      {fields.map((field) => {
        const value = (doc as any)[field];
        if (!value) return null;
        return (
          <div key={field} className="flex flex-col">
            <span className="text-sm text-gray-600 text-start">{labels[field]}</span>
            <span className="font-medium text-start">{value}</span>
          </div>
        );
      })}
    </div>
  );
};

const items = [
  {
    label: 'Opciones',
    items: [
      {
        label: <p className='text-red-600'>Eliminar</p>,
        icon: <MdDelete color={'#ff6467'} size={14}/>
      },
      {
        label: 'Editar',
        icon: 'pi pi-upload'
      }
    ]
  }
];

export const DocumentosAsociadosAccordion: React.FC<Props> = ({ documentos, setDocumentos }) => {
  const [descripciones, setDescripciones] = useState<Record<string, string>>({});
  const menuLeft = useRef<Menu>(null);

  useEffect(() => {
    const fetchDescripciones = async () => {
      const result: Record<string, string> = {};
      await Promise.all(
        documentos.map(async (doc) => {
          if (!doc.id) return;
          try {
            const res = await getOtrosDocumentosAsociadosById(doc.id);
            result[doc.id] = res?.descripcion || '';
          } catch {
            result[doc.id] = '';
          }
        })
      );
      setDescripciones(result);
    };
    if (documentos.length) {
      fetchDescripciones();
    }
  }, [documentos]);

  const eliminarDocumentoRelacionado = (e:any, doc:any) => {
    console.log(e, doc)
    console.log("ID", doc.id)

    const filter = documentos.filter((f) => f.id != doc.id)

    console.log(filter)

    setDocumentos(filter)

  }

  // const renderHeader = (doc: OtrosDocumentosAsociados) => (
  //   <div className="flex items-center justify-between w-full px-5">
  //     <div className="flex items-center gap-3">
  //       {getIcon(doc.codDocAsociado!)}
  //       <div className='flex flex-col text-start'>
  //         <h4 className="text-lg font-semibold">{doc.nombreDocAsociado}</h4>
  //         <small className="text-gray-500">Código: {doc.codDocAsociado}</small>
  //       </div>
  //     </div>
  //     <div>
  //     </div>
  //   </div>
  // );


  const renderHeader = (doc: OtrosDocumentosAsociados) => (
    <div className="flex items-center justify-between w-full px-5">
      <div className="flex items-center gap-3">
        {getIcon(doc.codDocAsociado!)}
        <div className='flex flex-col text-start'>
          <h4 className="text-lg font-semibold">{doc.nombreDocAsociado}</h4>
          <small className="text-gray-500">Código: {doc.codDocAsociado}</small>
        </div>
      </div>
      <div
        onClick={(e) => {
          e.stopPropagation(); // evita que se despliegue el acordeón
          // aquí va tu lógica para eliminar
          eliminarDocumentoRelacionado(e, doc)
          console.log('Eliminar', doc.codDocAsociado);
        }}
      >
        <div className='hover:bg-gray-200 p-1'>
          <IoClose size={20} />
        </div>
      </div>
    </div>
  );

  return (
    <Accordion multiple className="rounded-lg overflow-hidden">
      {documentos.map((doc) => (
        <AccordionTab key={doc.codDocAsociado} header={renderHeader(doc)}>
          {renderDetails(doc)}
        </AccordionTab>
      ))}
    </Accordion>
  );
};
