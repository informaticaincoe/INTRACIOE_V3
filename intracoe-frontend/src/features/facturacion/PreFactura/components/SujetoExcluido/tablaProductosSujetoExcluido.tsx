import { CuerpoDocumento, CuerpoDocumentoSujetoExcluido } from '../../interfaces/facturaPdfInterfaces';

interface TablaProductosSujetoExluidoInterface {
  productos: CuerpoDocumentoSujetoExcluido[];
  tipo_dte: string;
}

export const TablaProductosSujetoExcluido: React.FC<TablaProductosSujetoExluidoInterface> = ({
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
            <th className="border-border-color border-r-2 p-2">Unidad</th>
            <th className="border-border-color border-r-2 py-2 pl-4 text-start">
              Descripción
            </th>
            <th className="border-border-color border-r-2 p-2">
              Precio unitario
            </th>
            
            <th className="border-border-color border-r-2 p-2">
              Descuento por item
            </th>
            
            <th className="p-2">Ventas</th>
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
                {producto.uniMedida}
              </td>{' '}
              <td className="border-border-color border-t-2 border-r-2 p-2 pl-4 text-start">
                {producto.descripcion}
              </td>{' '}
              {/* descripcion productos */}
              <td className="border-border-color border-t-2 border-r-2 p-2 pl-4">
                $ {producto.precioUni}
              </td>{' '}
              <td className="border-border-color border-t-2 border-r-2 p-2 pl-4">
                $ {producto.montoDescu}
              </td>
              <td className="border-border-color border-t-2 border-r-2 p-2 pl-4">
                $ {producto.compra}
              </td>
              
            </tr>
          ))}
        </tbody>
      </table>
    </>
  );
};
