import { useEffect, useState } from "react";
import { Title } from "../../../shared/text/title";
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';

import { getAllActivities } from "../../facturacion/activities/services/activitiesServices";
import { getAllAmbientes } from "../../../shared/services/ambienteService";
import { getAllDescuentos } from "../../../shared/services/productos/productosServices";

type CatalogKey = 'catalogo' | 'ambientes' | 'descuentos';

// Cada valor es una función que recibe opcionalmente un filtro y devuelve Promise<any[]>
const fetchers: Record<CatalogKey, (filter?: string) => Promise<any[]>> = {
  catalogo: (filter = '') => getAllActivities(filter),
  ambientes: () => getAllAmbientes(),
  descuentos: () =>getAllDescuentos(),
}

export const CatalogosPage = () => {
  const [selectedCatalog, setSelectedCatalog] = useState<CatalogKey>('catalogo');
  const [filterTerm, setFilterTerm] = useState<string>('');      // si quieres filtrar
  const [data, setData] = useState<any[]>([]);
  const [loading, setLoading] = useState<boolean>(false);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        // Llamamos al fetcher correspondiente, pasándole filterTerm
        const result = await fetchers[selectedCatalog](filterTerm);
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

      <div className="grid grid-cols-[18%_82%] gap-10 p-10 h-full">
        {/* Sidebar */}
        <div className="bg-white p-5">
          <h2 className="font-semibold text-xl mb-4">Lista catálogos</h2>
          <ul className="flex flex-col gap-2 text-start">
            {(['catalogo', 'descuentos', 'ambientes'] as CatalogKey[]).map(key => (
              <li
                key={key}
                onClick={() => setSelectedCatalog(key)}
                className={
                  `px-2 py-2 rounded-md cursor-pointer ` +
                  (selectedCatalog === key
                    ? 'bg-blue-300 text-primary-blue'
                    : 'hover:bg-blue-100')
                }
              >
                {key.charAt(0).toUpperCase() + key.slice(1)}
              </li>
            ))}
          </ul>
        </div>

        {/* Contenido */}
        <div className="bg-white p-5">
          {loading
            ? <p>Cargando...</p>
            : (
              <DataTable value={data} responsiveLayout="scroll">
                {columns.map(col => (
                  <Column key={col.field} field={col.field} header={col.header} />
                ))}
              </DataTable>
            )
          }
        </div>
      </div>
    </>
  );
};
