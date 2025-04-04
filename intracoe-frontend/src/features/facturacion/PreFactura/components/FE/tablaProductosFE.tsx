import { CuerpoDocumento } from '../../interfaces/facturaPdfInterfaces';

interface TablaProductosFEInterface {
  productos: CuerpoDocumento[];
  tipo_dte: string;
}

export const TablaProductosFE: React.FC<TablaProductosFEInterface> = ({
  productos,
  tipo_dte,
}) => {
  return (
    <>
      <table className="border-border-color w-full table-auto rounded-md border-2 text-start">
        <thead>
          <tr className="text-center">
            <th className="border-border-color border-r-2 p-2 text-center">
              N°
            </th>
            <th className="border-border-color border-r-2 p-2">Cantidad:</th>
            <th className="border-border-color border-r-2 p-2">Código</th>
            <th className="border-border-color border-r-2 py-2 pl-4 text-start">
              Descripción
            </th>
            <th className="border-border-color border-r-2 p-2">
              Precio unitario
            </th>
            {tipo_dte == '03' && (
              <>
                <th className="border-border-color border-r-2 p-2">
                  IVA unitario
                </th>{' '}
                {/*Mostra el iva unitario si es un credito fiscal*/}
              </>
            )}
            <th className="border-border-color border-r-2 p-2">
              Otros montos no afectos
            </th>
            <th className="border-border-color border-r-2 p-2">
              Descuento por item
            </th>
            <th className="border-border-color border-r-2 p-2">
              Ventas no sujetas
            </th>
            <th className="border-border-color border-r-2 p-2">
              Ventas exentas
            </th>
            <th className="p-2">Ventas grabadas</th>
          </tr>
        </thead>

        <tbody className="">
          {productos.map((producto, index) => (
            <tr key={index}>
              <td className="border-border-color border-t-2 border-r-2 text-center">
                {index + 1}
              </td>{' '}
              {/* correlativo filas*/}
              <td className="border-border-color border-t-2 border-r-2 p-2 pl-4">
                {producto.cantidad}
              </td>{' '}
              {/* cantidad productos */}
              <td className="border-border-color border-t-2 border-r-2 p-2 pl-4">
                {producto.codigo}
              </td>{' '}
              {/* codigo productos */}
              <td className="border-border-color border-t-2 border-r-2 p-2 pl-4 text-start">
                {producto.descripcion}
              </td>{' '}
              {/* descripcion productos */}
              <td className="border-border-color border-t-2 border-r-2 p-2 pl-4">
                $ {producto.precioUni}
              </td>{' '}
              {/* precio unitario productos */}
              {tipo_dte == '03' && (
                <>
                  <td className="border-border-color border-t-2 border-r-2 p-2 pl-4">
                    $ {(producto.precioUni * 0.13).toFixed(2)}
                  </td>{' '}
                  {/* iva unitario */}
                </>
              )}
              <td className="border-border-color border-t-2 border-r-2 p-2 pl-4">
                $ {producto.ventaNoSuj}
              </td>
              <td className="border-border-color border-t-2 border-r-2 p-2 pl-4">
                $ {producto.ventaExenta}
              </td>
              <td className="border-border-color border-t-2 border-r-2 p-2 pl-4">
                $ {producto.ventaGravada}
              </td>
              <td className="border-border-color border-t-2 border-r-2 p-2 pl-4">
                $ 0.00
              </td>
              <td className="border-border-color border-t-2 border-r-2 p-2 pl-4">
                $ 0.00
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </>
  );
};
