import { Resumen } from '../../interfaces/facturaPdfInterfaces';

interface TablaResumentFEProps {
  resumen: Resumen;
}

export const TablaResumenFE: React.FC<TablaResumentFEProps> = ({ resumen }) => {
  return (
    <>
      <table className="border-border-color w-full table-fixed rounded-2xl border-2">
        <tbody>
          <tr className="">
            <td className="border-border-color border-2 px-3 py-1 text-end align-middle">
              Sumatoria de venta:
            </td>
            <td className="border-border-color border-2 px-3 py-1 text-start align-middle">
              $ {resumen.subTotalVentas}
            </td>
          </tr>
          <tr>
            <td className="border-border-color border-2 px-3 py-1 text-end align-middle">
              Monto gloabl Dec. Rebajas y otros a ventas no sujetas:
            </td>
            <td className="border-border-color border-2 px-3 py-1 text-start align-middle">
              $ {resumen.descuNoSuj}
            </td>
          </tr>
          <tr>
            <td className="border-border-color border-2 px-3 py-1 text-end align-middle">
              Otros montos Monto gloabl Dec. Rebajas y otros a ventas exentas:
            </td>
            <td className="border-border-color border-2 px-3 py-1 text-start align-middle">
              $ {resumen.descuExenta}
            </td>
          </tr>
          <tr>
            <td className="border-border-color border-2 px-3 py-1 text-end align-middle">
              Monto gloabl Dec. Rebajas y otros a ventas grabadas:
            </td>
            <td className="border-border-color border-2 px-3 py-1 text-start align-middle">
              $ {resumen.descuGravada}
            </td>
          </tr>
          <tr>
            <td className="border-border-color border-2 px-3 py-1 text-end align-middle">
              Sub-total:
            </td>
            <td className="border-border-color border-2 px-3 py-1 text-start align-middle">
              $ {resumen.subTotal}
            </td>
          </tr>
          <tr className="text-center">
            <td className="border-border-color border-2 px-3 py-1 text-end align-middle">
              Total IVA:
            </td>
            <td className="border-border-color border-2 px-3 py-1 text-start align-middle">
              $ {resumen.totalIva}
            </td>
          </tr>
          <tr className="text-center">
            <td className="border-border-color border-2 px-3 py-1 text-end align-middle">
              IVA retenido:
            </td>
            <td className="border-border-color border-2 px-3 py-1 text-start align-middle">
              $ {resumen.ivaRete}
            </td>
          </tr>
          <tr>
            <td className="border-border-color border-2 px-3 py-1 text-end align-middle">
              Retención de renta:
            </td>
            <td className="border-border-color border-2 px-3 py-1 text-start align-middle">
              $ {resumen.reteRenta}
            </td>
          </tr>
          <tr>
            <td className="border-border-color border-2 px-3 py-1 text-end align-middle">
              Monto total operación:
            </td>
            <td className="border-border-color border-2 px-3 py-1 text-start align-middle">
              $ {resumen.montoTotalOperacion}
            </td>
          </tr>
          <tr>
            <td className="border-border-color border-2 px-3 py-1 text-end align-middle">
              Total otros Montos No afectados:
            </td>
            <td className="border-border-color border-2 px-3 py-1 text-start align-middle">
              $ 0
            </td>
          </tr>
          <tr>
            <td className="border-border-color border-2 px-3 py-1 text-end align-middle">
              Total a pagar:
            </td>
            <td className="px-3 py-1 text-start align-middle">
              $ {resumen.totalPagar}
            </td>
          </tr>
        </tbody>
      </table>
    </>
  );
};
