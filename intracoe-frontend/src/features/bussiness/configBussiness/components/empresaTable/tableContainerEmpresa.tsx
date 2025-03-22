import { DataTable } from 'primereact/datatable';
import { WhiteSectionsPage } from '../../../../../shared/containers/whiteSectionsPage';
import { Column } from 'primereact/column';
import { useEffect, useState } from 'react';
import { getAllEmpresas } from '../../services/empresaServices';
import { Empresa } from '../../interfaces/empresaInterfaces';
import { ActionsEmpresa } from './actionsEmpresa';

export const TableContainerEmpresa = () => {
  const [empresasData, setEmpresasData] = useState<Empresa[]>([]);

  useEffect(() => {
    fetchEmpresas();
  }, []);

  const fetchEmpresas = async () => {
    try {
      const response = await getAllEmpresas();
      console.log(typeof response);
      console.log(response);

      setEmpresasData(response);
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <WhiteSectionsPage>
      <>
        <DataTable
          value={empresasData}
          paginator
          rows={5}
          rowsPerPageOptions={[5, 10, 25, 50]}
        >
          <Column field="nit" header={<p className="text-black">NIT</p>} />
          <Column
            field="nombre_comercial"
            header={<p className="text-black">NOMBRE</p>}
          />
          <Column
            header="ACCIONES"
            body={(empresasData: Empresa) => (
              <ActionsEmpresa empresa={empresasData} />
            )}
          />
        </DataTable>
      </>
    </WhiteSectionsPage>
  );
};
