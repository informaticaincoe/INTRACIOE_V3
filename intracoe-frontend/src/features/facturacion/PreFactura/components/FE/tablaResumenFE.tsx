import { resumenTablaFE } from "../../interfaces/facturaPdfInterfaces"

interface TablaResumentFEProps {
    resumen: resumenTablaFE
}

export const TablaResumenFE:React.FC<TablaResumentFEProps> = ({resumen}) => {
    return (
        <>
            <table className="table-fixed border-2 w-full border-border-color rounded-2xl">
                <tbody>
                    <tr className="">
                        <td className="align-middle py-1 px-3 border-2 border-border-color text-end">Sumatoria de venta:</td>
                        <td className="align-middle py-1 px-3 border-2 border-border-color text-start">$ {resumen.subTotalVentas}</td>
                    </tr>
                    <tr>
                        <td className="align-middle py-1 px-3 border-2 border-border-color text-end">Monto gloabl Dec. Rebajas y otros a ventas no sujetas:</td>
                        <td className="align-middle py-1 px-3 border-2 border-border-color text-start">$ {resumen.descuNoSuj}</td>
                    </tr>
                    <tr>
                        <td className="align-middle py-1 px-3 border-2 border-border-color text-end">Otros montos Monto gloabl Dec. Rebajas y otros a ventas exentas:</td>
                        <td className="align-middle py-1 px-3 border-2 border-border-color text-start">$ {resumen.descuExenta}</td>
                    </tr>
                    <tr>
                        <td className="align-middle py-1 px-3 border-2 border-border-color text-end">Monto gloabl Dec. Rebajas y otros a ventas grabadas:</td>
                        <td className="align-middle py-1 px-3 border-2 border-border-color text-start">$ {resumen.descuGravada}</td>
                    </tr>
                    <tr>
                        <td className="align-middle py-1 px-3 border-2 border-border-color text-end">Sub-total:</td>
                        <td className="align-middle py-1 px-3 border-2 border-border-color text-start">$ {resumen.subTotal}</td>
                    </tr>
                    <tr className="text-center">
                        <td className="align-middle py-1 px-3 border-2 border-border-color text-end">IVA retenido:</td>
                        <td className="align-middle py-1 px-3 border-2 border-border-color text-start">$ {resumen.ivaRete}</td>
                    </tr>
                    <tr>
                        <td className="align-middle py-1 px-3 border-2 border-border-color text-end">Retención de renta:</td>
                        <td className="align-middle py-1 px-3 border-2 border-border-color text-start">$ {resumen.reteRenta}
                        </td>
                    </tr>
                    <tr>
                        <td className="align-middle py-1 px-3 border-2 border-border-color text-end">Monto total operación:</td>
                        <td className="align-middle py-1 px-3 border-2 border-border-color text-start">$ {resumen.montoTotalOperacion}</td>
                    </tr>
                    <tr>
                        <td className="align-middle py-1 px-3 border-2 border-border-color text-end">Total otros Montos No afectados:</td>
                        <td className="align-middle py-1 px-3 border-2 border-border-color text-start">$ 0</td>
                    </tr>
                    <tr>
                        <td className="align-middle py-1 px-3 border-2 border-border-color text-end">Total a pagar:</td>
                        <td className="align-middle py-1 px-3 text-start">$ {resumen.totalPagar}</td>
                    </tr>
                </tbody>
            </table>
        </>
    )
}