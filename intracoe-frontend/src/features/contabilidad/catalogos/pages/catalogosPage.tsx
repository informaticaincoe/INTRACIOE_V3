import { SetStateAction, useEffect, useState } from "react";
import { Title } from "../../../../shared/text/title";
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';

import { getAllActivities, getAllAmbientes, getAllCondicioOperaciones, getAllDepartamentos, getAllDescuento, getAllIncoterms, getAllMetodosDePago, getAllTiposEstablecimientos, getAllModelosDeFacturacion, getAllMunicipios, getAllOtrosDocumentosAsociados, getAllPaises, getAllPlazos, getAllTipoContingencia, getAllTipoDocContingencia, getAllTipoDomicilioFiscal, getAllTipoDonacion, getAllTipoDTE, getAllTipoIdReceptor, getAllTipoInvalidacion, getAllTipoMoneda, getAllTipoPersona, getAllTipoRentencionIVA, getAllTipoServiciosMedicos, getAllTiposGeneracionDocumento, getAllTipoTransmision } from "../../../../shared/catalogos/services/catalogosServices";
import { HeaderTable } from "../components/headerTable";

type CatalogKey =
  'Actividades economicas' |
  'Ambientes' |
  'Modelo facturacion' |
  'Tipo transmision' |
  'Tipo contingencia' |
  'Tipo retencion IVA' |
  'Tipo generación de documento' |
  'Tipo establecimiento' |
  'Tipo servicio medico' |
  'tipo documento tributario electronico' |
  'Otros documentos asociados' |
  'Tipo de identificacion receptores' |
  'Paises' |
  'Departamentos' |
  'municipios' |
  'Condiciones de operación' |
  'Formas de pago' |
  'Plazos de pago' |
  'tipo de documento de contingencia' |
  'Tipo de invalidación' |
  'Tipo de donación' |
  'Tipo de persona' |
  'Tipo de transporte' |
  'Incoterms' |
  'Tipo de domicilio fiscal' |
  'Tipo de moneda' |
  'Descuento';

// Cada valor es una función que recibe opcionalmente un filtro y devuelve Promise<any[]>
const fetchers: Record<CatalogKey, (filter?: string) => Promise<any[]>> = {
  'Actividades economicas': (filter = '') => getAllActivities(filter),
  'Ambientes': () => getAllAmbientes(),
  'Modelo facturacion': () => getAllModelosDeFacturacion(),
  'Tipo transmision': () => getAllTipoTransmision(),
  'Tipo contingencia': () => getAllTipoContingencia(),
  'Tipo retencion IVA': () => getAllTipoRentencionIVA(),
  'Tipo generación de documento': () => getAllTiposGeneracionDocumento(),
  'Tipo establecimiento': () => getAllTiposEstablecimientos(),
  'Tipo servicio medico': () => getAllTipoServiciosMedicos(),
  'tipo documento tributario electronico': () => getAllTipoDTE(),
  'Otros documentos asociados': () => getAllOtrosDocumentosAsociados(),
  'Tipo de identificacion receptores': () => getAllTipoIdReceptor(),
  'Paises': () => getAllPaises(),
  'Departamentos': () => getAllDepartamentos(),
  'municipios': () => getAllMunicipios(),
  'Condiciones de operación': () => getAllCondicioOperaciones(),
  'Formas de pago': () => getAllMetodosDePago(),
  'Plazos de pago': () => getAllPlazos(),
  'tipo de documento de contingencia': () => getAllTipoDocContingencia(),
  'Tipo de invalidación': () => getAllTipoInvalidacion(),
  'Tipo de donación': () => getAllTipoDonacion(),
  'Tipo de persona': () => getAllTipoPersona(),
  'Tipo de transporte': () => getAllTipoPersona(),
  'Incoterms': () => getAllIncoterms(),
  'Tipo de domicilio fiscal': () => getAllTipoDomicilioFiscal(),
  'Tipo de moneda': () => getAllTipoMoneda(),
  'Descuento': () => getAllDescuento(),
}

export const CatalogosPage = () => {
  const [selectedCatalog, setSelectedCatalog] = useState<CatalogKey>('Actividades economicas');
  const [filterTerm, setFilterTerm] = useState<string>('');
  const [data, setData] = useState<any[]>([]);
  const [loading, setLoading] = useState<boolean>(false);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        // Llamamos al fetcher correspondiente, pasándole filterTerm
        const result = await (fetchers[selectedCatalog](filterTerm));
        setData(result);
      } catch (e) {
        console.error(e);
        setData([]);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [selectedCatalog, filterTerm]);

  // Genera columnas dinámicamente
  const columns = data.length
    ? Object.keys(data[0]).map(field => ({ field, header: field.toUpperCase() }))
    : [];

  return (
    <>
      <Title text="Catálogos" />

      <div className="grid grid-cols-[20%_80%] gap-10 p-10 h-[80vh] overflow-hidden">
        {/* Sidebar */}
        <div id="catalogos-list" className="bg-white overflow-y-auto max-h-[80vh] rounded-md">
          <span className="p-4 w-full flex flex-col">
            <h2 className="font-semibold text-xl pb-4 pt-4 sticky top-0 bg-white">Lista catálogos</h2>
            <ul className="flex flex-col gap-2 text-start">
              {(['Actividades economicas',
                'Ambientes',
                'Modelo facturacion',
                'Tipo transmision',
                'Tipo contingencia',
                'Tipo retencion IVA',
                'Tipo generación de documento',
                'Tipo establecimiento',
                'Tipo servicio medico',
                'tipo documento tributario electronico',
                'Otros documentos asociados',
                'Tipo de identificacion receptores',
                'Paises',
                'Departamentos',
                'municipios',
                'Condiciones de operación',
                'Formas de pago',
                'Plazos de pago',
                'tipo de documento de contingencia',
                'Tipo de invalidación',
                'Tipo de donación',
                'Tipo de persona',
                'Tipo de transporte',
                'Incoterms',
                'Tipo de domicilio fiscal',
                'Tipo de moneda',
                'Descuento'
              ] as CatalogKey[]).map(key => (
                <li
                  key={key}
                  onClick={() => setSelectedCatalog(key)}
                  className={
                    `px-2 py-2 rounded-md cursor-pointer ` +
                    (selectedCatalog === key
                      ? 'bg-blue-200 text-primary-blue'
                      : 'hover:bg-blue-100')
                  }
                >
                  {key.charAt(0).toUpperCase() + key.slice(1)}
                </li>
              ))}
            </ul>
          </span>
        </div>

        {/* Contenido */}
        <div className="bg-white p-5">
          {loading
            ? <p>Cargando...</p>
            : (
              <>
                <HeaderTable
                  nombre={selectedCatalog}
                  setActivities={function (): void { }}
                  filterTerm={filterTerm}
                  setFilterTerm={setFilterTerm}
                />
                <DataTable value={data} responsiveLayout="scroll">
                  {columns.map(col => {
                    return  col.header != "ID" && <Column key={col.field} field={col.field} header={col.header} /> //no mostrarel id
                  })}
                </DataTable>
              </>
              // <TableContainer data={data}/>
            )
          }
        </div>
      </div>
    </>
  );
};
