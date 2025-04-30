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
import { ProductosTabla } from '../FE/productosAgregados/productosData';

interface Props {
  facturasAjuste: FacturaPorCodigoGeneracionResponse[];
  setFacturasAjuste: React.Dispatch<
    React.SetStateAction<FacturaPorCodigoGeneracionResponse[]>
  >;
  setIdListProducts: React.Dispatch<React.SetStateAction<string[]>>;
  setCantidadListProducts: React.Dispatch<React.SetStateAction<string[]>>;
  setListProducts: React.Dispatch<React.SetStateAction<ProductosTabla[]>>;
}

export const TablaProductosFacturaNotasDebito: React.FC<Props> = ({
  facturasAjuste,
  setFacturasAjuste,
  setIdListProducts,
  setCantidadListProducts,
  setListProducts,
}) => {
  // --- estado local de selección usando clave compuesta
  const [seleccionados, setSeleccionados] = useState<Record<string, boolean>>({});

  // --- 1) Derivar arrays cada vez que cambien facturasAjuste o seleccionados
  useEffect(() => {
    // Filtramos y aplanamos todos los productos seleccionados
    const seleccion = facturasAjuste.flatMap((factura) =>
      factura.productos
        .filter((prod) =>
          seleccionados[
          `${factura.codigo_generacion}-${prod.producto_id}`
          ]
        )
        .map((prod) => ({
          facturaCodigo: factura.codigo_generacion,
          ...prod,
        }))
    );

    // Extraemos ids y cantidades
    const ids = seleccion.map((item) =>
      item.producto_id.toString()
    );
    const cantidades = seleccion.map((item) =>
      (item.cantidad_editada ?? item.cantidad).toString()
    );

    // Construimos la lista de ProductosTabla
    const productosTabla: ProductosTabla[] = seleccion.map((item) => ({
      id: item.producto_id,
      codigo: item.codigo,
      descripcion: item.descripcion,
      cantidad: item.cantidad_editada ?? item.cantidad,
      preunitario: parseFloat(item.precio_unitario),
      iva_unitario: parseFloat(item.iva_unitario),
      descuento: null,
      total_neto: 0,
      total_iva: 0,
      total_con_iva: 0,
      iva_percibido: 0,
      total_tributos: 0,
      seleccionar: true,
      imagen: '',
      categoria_id: null,
      tipo_item: null,
      unidad_medida_id: 0,
      tributo_id: 0,
      referencia_interna: '',
      maneja_lotes: false,
      fecha_vencimiento: null,
      creado: '',
      actualizado: '',
      precio_compra: 0,
      precio_venta: 0,
      precio_iva: false,
      stock: 0,
      stock_minimo: 0,
      stock_maximo: 0,
    }));

    setIdListProducts(ids);
    setCantidadListProducts(cantidades);
    setListProducts(productosTabla);
  }, [facturasAjuste, seleccionados, setIdListProducts, setCantidadListProducts, setListProducts]);

  // --- 2) Manejador de selección
  const handleSelect = (
    facturaCodigo: string,
    productoId: number,
    checked: boolean
  ) => {
    const key = `${facturaCodigo}-${productoId}`;
    setSeleccionados((prev) => ({ ...prev, [key]: checked }));
  };

  // --- 3) Manejador de cambio de cantidad
  const handleCantidadChange = (
    facturaCodigo: string,
    productoId: number,
    value: number | null
  ) => {
    setFacturasAjuste((prev) =>
      prev.map((factura) =>
        factura.codigo_generacion === facturaCodigo
          ? {
            ...factura,
            productos: factura.productos.map((prod) =>
              prod.producto_id === productoId
                ? { ...prod, cantidad_editada: value ?? 0 }
                : prod
            ),
          }
          : factura
      )
    );
  };

  // --- 4) Render
  return facturasAjuste.length > 0 ? (
    <Accordion multiple>
      {facturasAjuste.map((factura) => (
        <AccordionTab
          key={factura.codigo_generacion}
          header={
            <div className="grid grid-cols-[auto_1fr] gap-2 text-sm text-start">
              <span className="font-semibold">Código:</span>
              <span>{factura.codigo_generacion}</span>
              <span className="font-semibold">Control:</span>
              <span>{factura.num_documento}</span>
              <span className="font-semibold">Emisión:</span>
              <span>{factura.fecha_emision}</span>
              <span className="font-semibold">Receptor:</span>
              <span>{factura.receptor.nombre}</span>
              <span className="font-semibold">Total:</span>
              <span>${factura.total}</span>
            </div>
          }
        >
          <DataTable
            value={factura.productos}
            tableStyle={{ minWidth: '50rem' }}
            paginator
            rows={5}
            rowsPerPageOptions={[5, 10, 25, 50]}
          >
            <Column
              header="Seleccionar"
              body={(row: FacturaDetalleItem) => {
                const key = `${factura.codigo_generacion}-${row.producto_id}`;
                return (
                  <Checkbox
                    checked={!!seleccionados[key]}
                    onChange={(e) =>
                      handleSelect(
                        factura.codigo_generacion,
                        row.producto_id,
                        e.checked ?? false
                      )
                    }
                  />
                );
              }}
            />
            <Column
              header="Producto"
              body={(row) => (
                <>{`${row.codigo} - ${row.descripcion}`}</>
              )}
            />
            <Column
              header="Precio Unit."
              body={(row: FacturaDetalleItem) => {
                // parseamos a número antes de formatear
                const precio = Number(row.precio_unitario) || 0;
                return <>${precio.toFixed(2)}</>;
              }}
            />

            <Column
              header="Cantidad"
              body={(row) => {
                const key = `${factura.codigo_generacion}-${row.producto_id}`;
                return (
                  <InputNumber
                    value={row.cantidad_editada ?? row.cantidad}
                    onValueChange={(
                      e: InputNumberValueChangeEvent
                    ) =>
                      handleCantidadChange(
                        factura.codigo_generacion,
                        row.producto_id,
                        e.value ?? 1
                      )
                    }
                    disabled={!seleccionados[key]}
                  />
                );
              }}
            />
          </DataTable>
        </AccordionTab>
      ))}
    </Accordion>
  ) : null;
};
