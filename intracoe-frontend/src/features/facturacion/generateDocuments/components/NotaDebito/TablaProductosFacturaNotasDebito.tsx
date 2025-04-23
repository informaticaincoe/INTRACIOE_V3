import { Column } from 'primereact/column';
import { DataTable } from 'primereact/datatable';
import {
  InputNumber,
  InputNumberValueChangeEvent,
} from 'primereact/inputnumber';
import { Checkbox } from 'primereact/checkbox';
import { Accordion, AccordionTab } from 'primereact/accordion';
import React, { useEffect, useState } from 'react';
import {
  FacturaDetalleItem,
  FacturaPorCodigoGeneracionResponse,
} from '../../../../../shared/interfaces/interfaces';

interface TablaProductosFacturaNotasDebitoProps {
  facturasAjuste: FacturaPorCodigoGeneracionResponse[];
  setFacturasAjuste: any;
  setIdListProducts: any;
  setCantidadListProducts: any;
  setListProducts: any;
}

export const TablaProductosFacturaNotasDebito: React.FC<
  TablaProductosFacturaNotasDebitoProps
> = ({
  facturasAjuste,
  setFacturasAjuste,
  setIdListProducts,
  setCantidadListProducts,
  setListProducts,
}) => {
  const [seleccionados, setSeleccionados] = useState<{
    [key: string]: boolean;
  }>({});

  useEffect(() => {
    // actualizarListasSeleccionadas(seleccionados);
  }, [facturasAjuste, seleccionados]);

  useEffect(() => {
    console.log('facturasAjuste', facturasAjuste);
    if (facturasAjuste) {
    }
  }, [facturasAjuste]);

  const handleCantidadChange = (
    value: number | null,
    facturaCodigo: string,
    productoId: number
  ) => {
    const nuevaLista = facturasAjuste.map((factura) => {
      if (factura.codigo_generacion === facturaCodigo) {
        return {
          ...factura,
          productos: factura.productos.map((producto) =>
            producto.producto_id === productoId
              ? { ...producto, cantidad_editada: value ?? 0 }
              : producto
          ),
        };
      }
      return factura;
    });

    setFacturasAjuste(nuevaLista);
  };

  const handleMontoAumentarChange = (
    value: number | null,
    facturaCodigo: string,
    productoId: number
  ) => {
    const nuevaLista = facturasAjuste.map((factura) => {
      if (factura.codigo_generacion === facturaCodigo) {
        return {
          ...factura,
          productos: factura.productos.map((producto) =>
            producto.producto_id === productoId
              ? { ...producto, monto_a_aumentar: value ?? 0 }
              : producto
          ),
        };
      }
      return factura;
    });

    setFacturasAjuste(nuevaLista);
  };

  const handleSelectChange = (checked: boolean, id: string) => {
    setSeleccionados((prev) => {
      const actualizados = {
        ...prev,
        [id]: checked,
      };
      // actualizarListasSeleccionadas(actualizados);
      return actualizados;
    });
  };

  // const actualizarListasSeleccionadas = (seleccionadosActuales: {
  //   [key: string]: boolean;
  // }) => {
  //   const productosSeleccionados: string[] = [];
  //   const cantidadesSeleccionadas: string[] = [];
  //   const productosTabla: ProductosTabla[] = [];

  //   facturasAjuste.forEach((factura) => {
  //     factura.productos.forEach((producto) => {
  //       const idStr = producto.producto_id.toString();
  //       if (seleccionadosActuales[idStr]) {
  //         productosSeleccionados.push(idStr);
  //         const cantidadFinal = producto.cantidad_editada ?? producto.cantidad;
  //         cantidadesSeleccionadas.push(cantidadFinal.toString());

  //         // Armar objeto del tipo ProductosTabla
  //         // productosTabla.push({
  //         //   id: producto.producto_id,
  //         //   codigo: producto.codigo,
  //         //   descripcion: producto.descripcion,
  //         //   cantidad: cantidadFinal,
  //         //   preunitario: parseFloat(producto.precio_unitario),
  //         //   iva_unitario: parseFloat(producto.iva_unitario),
  //         //   // no_grabado: false,
  //         //   descuento: null,
  //         //   total_neto: 0,
  //         //   total_iva: 0,
  //         //   total_con_iva: 0,
  //         //   iva_percibido: 0,
  //         //   total_tributos: 0,
  //         //   seleccionar: false,
  //         // });
  //       }
  //     });
  //   });

  //   setIdListProducts(productosSeleccionados);
  //   setCantidadListProducts(cantidadesSeleccionadas);
  //   setListProducts(productosTabla);
  // };

  return (
    <>
      {facturasAjuste.length > 0 && (
        <Accordion multiple>
          {facturasAjuste.map((factura) => {
            const header = (
              <div className="grid grid-cols-[auto_1fr] gap-x-5 gap-y-2 text-start text-sm">
                <p className="font-semibold text-black">
                  Código de generación:
                </p>
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
                          handleSelectChange(
                            !!e.checked,
                            rowData.producto_id.toString()
                          )
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
                          handleCantidadChange(
                            e.value ?? null,
                            factura.codigo_generacion,
                            rowData.producto_id
                          )
                        }
                        disabled={
                          !seleccionados[rowData.producto_id.toString()]
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
