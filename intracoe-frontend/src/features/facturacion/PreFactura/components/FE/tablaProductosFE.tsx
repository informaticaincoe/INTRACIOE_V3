import { useEffect } from "react"
import { CuerpoDocumento } from "../../interfaces/facturaPdfInterfaces"

interface TablaProductosFEInterface {
    productos: CuerpoDocumento[]
}

export const TablaProductosFE: React.FC<TablaProductosFEInterface> = ({ productos }) => {

    useEffect(() => {
        console.log("productos", productos)
        console.log(typeof (productos))

    }, [])
    return (
        <>
            <table className="table-auto border w-full border-border-color text-start rounded-md ">
                <thead className="rounded-md">
                    <tr className="text-center">
                        <td className="p-2 border-r border-border-color text-center">N°</td>
                        <td className="p-2 border-r border-border-color">Cantidad:</td>
                        <td className="p-2 border-r border-border-color">Código</td>
                        <td className="p-2 border-r border-border-color">Descripción</td>
                        <td className="p-2 border-r border-border-color">Precio unitario</td>
                        <td className="p-2 border-r border-border-color">Otros montos no afectos</td>
                        <td className="p-2 border-r border-border-color">Descuento por item</td>
                        <td className="p-2 border-r border-border-color">Ventas no sujetas</td>
                        <td className="p-2 border-r border-border-color">Ventas exentas</td>
                        <td className="p-2">Ventas grabadas</td>
                    </tr>

                </thead>
                <tbody className="pb-5">
                    {
                        productos.map((producto, index) => (
                            <tr>
                                <td className="border-r border-t border-border-color text-center">{index + 1}</td>
                                <td className="p-2 border-r border-t border-border-color pl-4">{producto.cantidad}</td>
                                <td className="p-2 border-r border-t border-border-color pl-4">{producto.codigo}</td>
                                <td className="p-2 border-r border-t border-border-color pl-4">{producto.descripcion}</td>
                                <td className="p-2 border-r border-t border-border-color pl-4">$ {producto.precioUni}</td>
                                <td className="p-2 border-r border-t border-border-color pl-4">$ 0</td> {/* TODO: */}
                                <td className="p-2 border-r border-t border-border-color pl-4">$ {producto.montoDescu}</td>
                                <td className="p-2 border-r border-t border-border-color pl-4">$ {producto.ventaNoSuj}</td>
                                <td className="p-2 border-r border-t border-border-color pl-4">$ {producto.ventaExenta}</td>
                                <td className="p-2 border-r border-t border-border-color pl-4">$ {producto.ventaGravada}</td>
                            </tr>
                        ))
                    }
                </tbody>
            </table>
        </>
    )
}