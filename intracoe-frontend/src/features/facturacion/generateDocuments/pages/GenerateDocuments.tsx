import { Divider } from 'primereact/divider';
import { WhiteSectionsPage } from '../../../../shared/containers/whiteSectionsPage';
import { Title } from '../../../../shared/text/title';
import { useEffect, useState } from 'react';
import { getAllEmpresas } from '../../../bussiness/configBussiness/services/empresaServices';
import { TipoDeDocumento } from '../components/tipoDeDocumento';
import { getAllTipoDte } from '../services/tipoDte';
import { SeccionconfiguracionFactura } from '../components/configuracionFactura/SeccionconfiguracionFactura';

export const GenerateDocuments = () => {
  const [emisorData, setEmisorData] = useState({
    nit: '',
    nombre: '',
    telefono: '',
    email: '',
    direccion_comercial: ''
  })

  const [tipoDte, setTipoDte] = useState(null);  // Usamos 'null' al principio porque es el valor inicial
  const [tipoDteLista, setTipoDteLista] = useState([]);  // Lista de tipos de documentos

  useEffect(() => {
    fetchEmisarInfo()
    fetchTipoDte()
  }, [])

  const fetchEmisarInfo = async () => {
    try {
      const response = await getAllEmpresas()
      setEmisorData({
        nit: response[0].nit,
        nombre: response[0].nombre_razon_social,
        telefono: response[0].telefono,
        email: response[0].email,
        direccion_comercial: response[0].direccion_comercial
      })
    } catch (error) {
      console.log(error)
    }
  }

  const fetchTipoDte = async () => {
    try {
      const response = await getAllTipoDte();

      // Transformamos la respuesta en el formato adecuado para el Dropdown
      setTipoDteLista(response.map((documento: { descripcion: any; id: any; }) => ({
        label: documento.descripcion,  // Texto que se muestra en la lista
        value: documento.id,           // Valor que se asigna al seleccionar una opción
      })));
      
    } catch (error) {
      console.log(error);
    }
  };
  

  return (
    <>
      <Title text="Generar documentos" />

      <TipoDeDocumento nit={emisorData.nit} nombre={emisorData.nombre} telefono={emisorData.telefono} email={emisorData.email} direccion_comercial={emisorData.direccion_comercial} />

      <SeccionconfiguracionFactura 
        tipoDteLista={tipoDteLista} 
        setTipoDte={setTipoDte}
        tipoDte={tipoDte}
      />
    </>
  );
};
