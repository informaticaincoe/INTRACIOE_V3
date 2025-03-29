import { Column } from 'primereact/column';
import { DataTable } from 'primereact/datatable';
import { InputNumber, InputNumberValueChangeEvent } from 'primereact/inputnumber';
import { Checkbox } from 'primereact/checkbox';
import { Accordion, AccordionTab } from 'primereact/accordion';
import React, { useEffect, useState } from 'react';
import { FacturaDetalleItem, FacturaPorCodigoGeneracionResponse } from '../../../../../shared/interfaces/interfaces';

interface TablaProductosFacturaNotasDebitoProps {
  facturasAjuste: FacturaPorCodigoGeneracionResponse[];
  setFacturasAjuste: any
}

export const TablaProductosFacturaNotasDebito: React.FC<TablaProductosFacturaNotasDebitoProps> = ({
  facturasAjuste,
  setFacturasAjuste,
}) => {
  const [seleccionados, setSeleccionados] = useState<{ [key: string]: boolean }>({});

  useEffect(() => {
    console.log("facturasAjuste", facturasAjuste)
  }, [facturasAjuste])
  const handleCantidadChange = (value: number | null, facturaCodigo: string, productoId: number) => {
    const nuevaLista = facturasAjuste.map(factura => {
      if (factura.codigo_generacion === facturaCodigo) {
        return {
          ...factura,
          productos: factura.productos.map(producto =>
            producto.producto_id === productoId
              ? { ...producto, cantidad_editada: value ?? 0 }
              : producto
          )
        };
      }
      return factura;
    });

    setFacturasAjuste(nuevaLista);
  };

  const handleMontoAumentarChange = (value: number | null, facturaCodigo: string, productoId: number) => {
    const nuevaLista = facturasAjuste.map(factura => {
      if (factura.codigo_generacion === facturaCodigo) {
        return {
          ...factura,
          productos: factura.productos.map(producto =>
            producto.producto_id === productoId
              ? { ...producto, monto_a_aumentar: value ?? 0 }
              : producto
          )
        };
      }
      return factura;
    });

    setFacturasAjuste(nuevaLista);
  };

  const handleSelectChange = (checked: boolean, id: string) => {
    setSeleccionados((prev) => ({
      ...prev,
      [id]: checked,
    }));
  };

  return (
    <>
      {facturasAjuste.length > 0 && (
        <Accordion multiple>
          {facturasAjuste.map((factura) => {
            const header = (
              <div className="grid grid-cols-[auto_1fr] gap-x-5 gap-y-2 text-sm text-start">
                <p className="font-semibold text-black">Código de generación:</p>
                <p className="text-gray-700">{factura.codigo_generacion}</p>
                <p className="font-semibold text-black">Número de control:</p>
                <p className="text-gray-700">{factura.num_documento}</p>
                <p className="font-semibold text-black">Fecha emisión:</p>
                <p className="text-gray-700">{factura.fecha_emision}</p>
                <p className="font-semibold text-black">Receptor:</p>
                <p className="text-gray-700">{factura.receptor.nombre}</p>
                <p className="font-semibold text-black">Monto total:</p>
                <p className="text-gray-700">${factura.total}</p>
              </div>
            );

            return (
              <AccordionTab key={factura.codigo_generacion} header={header}>
                <DataTable
                  value={factura.productos}
                  tableStyle={{ minWidth: '50rem' }}
                  paginator
                  rows={5}
                  rowsPerPageOptions={[5, 10, 25, 50]}
                >
                  <Column
                    header={<p className="text-sm">SELECCIONAR</p>}
                    body={(rowData: FacturaDetalleItem) => (
                      <Checkbox
                        checked={!!seleccionados[rowData.producto_id]}
                        onChange={(e) =>
                          handleSelectChange(!!e.checked, rowData.producto_id.toString())
                        }
                      />
                    )}
                  />
                  <Column
                    header={<p className="text-sm">PRODUCTO</p>}
                    body={(rowData: FacturaDetalleItem) => (
                      <p>
                        {rowData.codigo} - {rowData.descripcion}
                      </p>
                    )}
                  />
                  <Column
                    header={<p className="text-sm">PRECIO UNITARIO</p>}
                    body={(rowData: FacturaDetalleItem) => (
                      <p>${rowData.precio_unitario}</p>
                    )}
                  />
                  <Column
                    header={<p className="text-sm">CANTIDAD</p>}
                    body={(rowData: FacturaDetalleItem) => (
                      <InputNumber
                        value={rowData.cantidad_editada ?? rowData.cantidad}
                        onValueChange={(e: InputNumberValueChangeEvent) =>
                          handleCantidadChange(e.value ?? null, factura.codigo_generacion, rowData.producto_id)
                        }
                      />
                    )}
                  />
                  <Column
                    header={<p className="text-sm">MONTO A AUMENTAR</p>}
                    body={(rowData: FacturaDetalleItem) => (
                      <InputNumber
                        value={rowData.monto_a_aumentar ?? 0}
                        onValueChange={(e: InputNumberValueChangeEvent) =>
                          handleMontoAumentarChange(e.value ?? null, factura.codigo_generacion, rowData.producto_id)
                        }
                        
                      />
                    )}
                  />
                </DataTable>
              </AccordionTab>
            );
          })}
        </Accordion>
      )}
    </>
  );
};
