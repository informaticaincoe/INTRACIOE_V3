import React, { useEffect } from 'react'
import { ResumenSujetoExcluido } from '../../interfaces/sujetoExcluidoInterfaces'

interface TablaResumenSujetoExcluidoProps {
    resumen: ResumenSujetoExcluido
}

export const TablaResumenSujetoExcluido: React.FC<TablaResumenSujetoExcluidoProps> = ({ resumen }) => {
    useEffect(() => {
        console.log("RESUMEN DENTRO DE TABLA", resumen)
    }, [resumen])

    return (
        <>
            <table className="border-border-color w-full table-fixed rounded-2xl border-2">
                <tbody>
                    <tr className="">
                        <td className="border-border-color border-2 px-3 py-1 text-end align-middle">
                            Sumatoria de venta:
                        </td>
                        <td className="border-border-color border-2 px-3 py-1 text-start align-middle">
                            $ {resumen.totalCompra}
                        </td>
                    </tr>
                    <tr>
                        <td className="border-border-color border-2 px-3 py-1 text-end align-middle">
                            Sub-Total:
                        </td>
                        <td className="border-border-color border-2 px-3 py-1 text-start align-middle">
                            $ {resumen.subTotal}
                        </td>
                    </tr>
                    <tr>
                        <td className="border-border-color border-2 px-3 py-1 text-end align-middle">
                            Total a pagar:
                        </td>
                        <td className="border-border-color border-2 px-3 py-1 text-start align-middle">
                            $ {resumen.totalPagar}
                        </td>
                    </tr>

                </tbody>
            </table>
        </>
    )
}
