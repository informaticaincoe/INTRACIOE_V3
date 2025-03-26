import { resumenTablaFE } from "../../interfaces/facturaPdfInterfaces"

interface TablaResumentFEProps {
    resumen: resumenTablaFE
}

export const TablaResumenFE:React.FC<TablaResumentFEProps> = ({resumen}) => {
    return (
        <>
            <table className="table-fixed border w-full border-border-color text-start rounded-md">
                <tr className="text-center">
                    <td className="py-2 px-4 border border-border-color text-end">Sumatoria de venta:</td>
                    <td className="py-2 px-4 border border-border-color text-start">$ {resumen.subTotalVentas}</td>
                </tr>
                <tr>
                    <td className="py-2 px-4 border border-border-color text-end">Monto gloabl Dec. Rebajas y otros a ventas no sujetas:</td>
                    <td className="py-2 px-4 border border-border-color text-start">$ {resumen.descuNoSuj}</td>
                </tr>
                <tr>
                    <td className="py-2 px-4 border border-border-color text-end">Otros montos Monto gloabl Dec. Rebajas y otros a ventas exentas:</td>
                    <td className="py-2 px-4 border border-border-color text-start">$ {resumen.descuExenta}</td>
                </tr>
                <tr>
                    <td className="py-2 px-4 border border-border-color text-end">Monto gloabl Dec. Rebajas y otros a ventas grabadas:</td>
                    <td className="py-2 px-4 border border-border-color text-start">$ {resumen.descuGravada}</td>
                </tr>
                <tr>
                    <td className="py-2 px-4 border border-border-color text-end">Sub-total:</td>
                    <td className="py-2 px-4 border border-border-color text-start">$ {resumen.subTotal}</td>
                </tr>
                <tr className="text-center">
                    <td className="py-2 px-4 border border-border-color text-end">IVA retenido:</td>
                    <td className="py-2 px-4 border border-border-color text-start">$ {resumen.ivaRete}</td>
                </tr>
                <tr>
                    <td className="py-2 px-4 border border-border-color text-end">Retención de renta:</td>
                    <td className="py-2 px-4 border border-border-color text-start">$ {resumen.reteRenta}
                    </td>
                </tr>
                <tr>
                    <td className="py-2 px-4 border border-border-color text-end">Monto total operación:</td>
                    <td className="py-2 px-4 border border-border-color text-start">$ {resumen.montoTotalOperacion}</td>
                </tr>
                <tr>
                    <td className="py-2 px-4 border border-border-color text-end">Total otros Montos No afectados:</td>
                    <td className="py-2 px-4 border border-border-color text-start"></td>
                </tr>
                <tr>
                    <td className="py-2 px-4 border border-border-color text-end">Total a pagar:</td>
                    <td className="py-2 px-4">$ {resumen.totalPagar}</td>
                </tr>
            </table>
        </>
    )
}