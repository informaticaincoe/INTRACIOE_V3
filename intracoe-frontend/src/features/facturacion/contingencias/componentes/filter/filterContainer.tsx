import { Dropdown, DropdownChangeEvent } from 'primereact/dropdown';
import { getAllTipoDte } from '../../../generateDocuments/services/configuracionFactura/configuracionFacturaService';
import { useEffect, useState } from 'react';

interface FilterContainerProps {
  filters: any;
  setFilters: any;
}

export const FilterContainer: React.FC<FilterContainerProps> = ({
  filters,
  setFilters,
}) => {
  // Inicialmente, el array contiene la opción "Todos"
  const [tipoDocumento, setTipoDocumento] = useState<any[]>([
    { name: 'Todos', code: null },
  ]);

  useEffect(() => {
    const fetchTipoDte = async () => {
      try {
        const response = await getAllTipoDte();
        const opciones = response.map(
          (documento: { descripcion: any; id: any }) => ({
            name: documento.descripcion,
            code: documento.id,
          })
        );
        // Se agrega la opción "Todos" al inicio y luego las demás opciones
        setTipoDocumento([{ name: 'Todos', code: null }, ...opciones]);
      } catch (error) {
        console.log(error);
      }
    };

    fetchTipoDte();
  }, []);

  useEffect(() => {
    console.log('TIPO DOCUMENTO', tipoDocumento);
  }, [filters.tipo_dte]);

  const booleanOptions = [
    { name: 'Todos', code: null },
    { name: 'Si', code: true },
    { name: 'No', code: false },
  ];

  const estadoFacturaFilters = [
    { name: 'Todos', code: null },
    { name: 'Enviados', code: true },
    { name: 'invalidados', code: false },
  ];

  const estadoInvalidacionFilters = [
    { name: 'Todos', code: null },
    { name: 'Enviados', code: 'viva' },
    { name: 'Invalidados', code: 'invalidada' },
    { name: 'En proceso invalidacion', code: 'enproceso' },
    { name: 'Firma pendiente', code: 'firmar' },
  ];

  return (
    <div className="flex gap-10 pt-5 pb-10">
      <span>
        <p>Recibidos por hacienda:</p>
        <Dropdown
          value={filters.recibido_mh}
          options={booleanOptions}
          optionLabel="name"
          optionValue="code"
          placeholder=""
          className="w-full text-start"
          onChange={(e: DropdownChangeEvent) =>
            setFilters({
              ...filters,
              recibido_mh: e.value,
            })
          }
          checkmark={true}
          highlightOnSelect={false}
        />
      </span>
      <span>
        <p>Tiene sello de recepción:</p>
        <Dropdown
          value={filters.has_sello_recepcion}
          options={booleanOptions}
          optionLabel="name"
          optionValue="code"
          placeholder=""
          className="w-full text-start"
          onChange={(e: DropdownChangeEvent) =>
            setFilters({
              ...filters,
              has_sello_recepcion: e.value,
            })
          }
          checkmark={true}
          highlightOnSelect={false}
        />
      </span>
      <span>
        <p className="text-start">Estado:</p>
        <Dropdown
          value={filters.estado_invalidacion}
          options={estadoInvalidacionFilters}
          optionLabel="name"
          optionValue="code"
          placeholder=""
          style={{ width: '10vw' }}
          className="w-8rem text-start"
          onChange={(e: DropdownChangeEvent) =>
            setFilters({
              ...filters,
              estado_invalidacion: e.value,
            })
          }
          checkmark={true}
          highlightOnSelect={false}
        />
      </span>
      <span>
        <p className="text-start">Tipo de factura:</p>
        <Dropdown
          value={filters.tipo_dte}
          options={tipoDocumento}
          optionLabel="name"
          optionValue="code"
          placeholder=""
          className="w-5rem text-start"
          onChange={(e: DropdownChangeEvent) =>
            setFilters({
              ...filters,
              tipo_dte: e.value,
            })
          }
          checkmark={true}
          highlightOnSelect={false}
        />
      </span>
    </div>
  );
};
