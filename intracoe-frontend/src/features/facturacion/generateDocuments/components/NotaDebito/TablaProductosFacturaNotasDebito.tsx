import { Column } from 'primereact/column';
import { DataTable } from 'primereact/datatable';
import {
  InputNumber,
  InputNumberValueChangeEvent,
} from 'primereact/inputnumber';
import { Checkbox } from 'primereact/checkbox';
import { Accordion, AccordionTab } from 'primereact/accordion';
import React, { useEffect, useRef, useState } from 'react';
import {
  FacturaDetalleItem,
  FacturaPorCodigoGeneracionResponse,
} from '../../../../../shared/interfaces/interfaces';
import { ProductosTabla } from '../FE/productosAgregados/productosData';
import CustomToast, { CustomToastRef, ToastSeverity } from '../../../../../shared/toast/customToast';
import { IoMdCloseCircle } from 'react-icons/io';

interface Props {
  facturasAjuste: FacturaPorCodigoGeneracionResponse[];
  setFacturasAjuste: React.Dispatch<
    React.SetStateAction<FacturaPorCodigoGeneracionResponse[]>
  >;
  setIdListProducts: React.Dispatch<React.SetStateAction<string[]>>;
  setCantidadListProducts: React.Dispatch<React.SetStateAction<string[]>>;
  setListProducts: React.Dispatch<React.SetStateAction<ProductosTabla[]>>;
  tipoDte:any
}

export const TablaProductosFacturaNotasDebito: React.FC<Props> = ({
  facturasAjuste,
  setFacturasAjuste,
  setIdListProducts,
  setCantidadListProducts,
  setListProducts,
  tipoDte
}) => {
  // --- estado local de selección usando clave compuesta
  const [seleccionados, setSeleccionados] = useState<Record<string, boolean>>({});
  const toastRef = useRef<CustomToastRef>(null);

  const handleAccion = (
    severity: ToastSeverity,
    icon: any,
    summary: string
  ) => {
    toastRef.current?.show({
      severity: severity,
      summary: summary,
      icon: icon,
      life: 2000,
    });
  };

  useEffect(() => {
    console.log("Factura Ajuste en tabla", facturasAjuste)
  }, [facturasAjuste])

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
    setFacturasAjuste(prev => {
      // 1) Clonamos todo el array de facturas
      const facturas = [...prev];

      // 2) Buscamos la factura
      const fi = facturas.findIndex(f => f.codigo_generacion === facturaCodigo);
      if (fi < 0) return prev;

      // 3) Clonamos su array de productos
      const productos = [...facturas[fi].productos];

      // 4) Buscamos el producto dentro de esa factura
      const pi = productos.findIndex(p => p.producto_id === productoId);
      if (pi < 0) return prev;

      if (value)
        if (tipoDte == '05' && value < productos[pi].cantidad) { //**nota de credito: la cantidad a anular no puedo ser mayor al de la factura
          // 5) Actualizamos sólo ese producto
          productos[pi] = {
            ...productos[pi],
            cantidad_editada: value ?? 0
          };

          // 6) Reemplazamos el array de productos en la factura
          facturas[fi] = {
            ...facturas[fi],
            productos
          };
        }
        else if (tipoDte == '06' ) { //**nota de debito: la cantidad a anular no puedo ser mayor al de la factura
          // 5) Actualizamos sólo ese producto
          productos[pi] = {
            ...productos[pi],
            cantidad_editada: value ?? 0
          };

          // 6) Reemplazamos el array de productos en la factura
          facturas[fi] = {
            ...facturas[fi],
            productos
          };
        }
        else {
          handleAccion(
            'error',
            <IoMdCloseCircle size={68} />,
            "La cantidad a anular es mayor a la cantidad de la factura"
          );
          console.error("error")
        }

      console.log("cantidad", productos[pi].cantidad)
      console.log("value", value)



      return facturas;
    });
  };

  const eliminarfacturaAdjunta = (codigo:string) => {
    const facturasFiltradas = facturasAjuste.filter(f => f.codigo_generacion != codigo)
    console.log(facturasFiltradas)
    setFacturasAjuste(facturasFiltradas)
  }


  // --- 4) Render
  return facturasAjuste.length > 0 ? (
    <>
      <CustomToast ref={toastRef} />
      <Accordion multiple>
        {facturasAjuste.map((factura) => (
          <AccordionTab
            key={factura.codigo_generacion}
            header={
              <div className='flex justify-between'>
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
                <button className='' onClick={()=> eliminarfacturaAdjunta(factura.codigo_generacion)}>eliminar</button>
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
    </>
  ) : null;
};
