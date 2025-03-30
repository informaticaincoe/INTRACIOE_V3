import { useEffect } from "react"
import { CuerpoDocumento } from "../../interfaces/facturaPdfInterfaces"

interface TablaProductosFEInterface {
    productos: CuerpoDocumento[]
    tipo_dte: string
}

export const TablaProductosFE: React.FC<TablaProductosFEInterface> = ({ productos, tipo_dte }) => {
    useEffect(() => {
        console.log("PRODUCTOS", productos)
        console.log(typeof (productos))
    }, [productos])

    return (
        <>
            <table className="table-auto border-2 w-full border-border-color text-start rounded-md ">
                <thead>
                    <tr className="text-center">
                        <th className="p-2 border-r-2 border-border-color text-center">N°</th>
                        <th className="p-2 border-r-2 border-border-color">Cantidad:</th>
                        <th className="p-2 border-r-2 border-border-color">Código</th>
                        <th className="py-2 pl-4 border-r-2 border-border-color text-start">Descripción</th>
                        <th className="p-2 border-r-2 border-border-color">Precio unitario</th>
                        {tipo_dte == '03' &&
                            <>
                                <th className="p-2 border-r-2 border-border-color">IVA unitario</th>
                                {/* <th className="p-2 border-r-2 border-border-color">Precio unitario neto</th> */}
                            </>
                        }
                        <th className="p-2 border-r-2 border-border-color">Otros montos no afectos</th>
                        <th className="p-2 border-r-2 border-border-color">Descuento por item</th>
                        <th className="p-2 border-r-2 border-border-color">Ventas no sujetas</th>
                        <th className="p-2 border-r-2 border-border-color">Ventas exentas</th>
                        <th className="p-2">Ventas grabadas</th>
                    </tr>
                </thead>


                <tbody className="">
                    {
                        productos.map((producto, index) => (
                            <tr key={index}>
                                <td className="border-r-2 border-t-2 border-border-color text-center">{index + 1}</td> {/* correlativo filas*/}
                                <td className="p-2 border-r-2 border-t-2 border-border-color pl-4">{producto.cantidad}</td> {/* cantidad productos */}
                                <td className="p-2 border-r-2 border-t-2 border-border-color pl-4">{producto.codigo}</td> {/* codigo productos */}
                                <td className="p-2 border-r-2 border-t-2 border-border-color pl-4 text-start">{producto.descripcion}</td> {/* descripcion productos */}
                                <td className="p-2 border-r-2 border-t-2 border-border-color pl-4">$ {(producto.precioUni)}</td> {/* precio unitario productos */}
                                {tipo_dte == '03' &&
                                    <>
                                        <td className="p-2 border-r-2 border-t-2 border-border-color pl-4">$ {(producto.precioUni * 0.13).toFixed(2)}</td> {/* iva unitario */}
                                        {/* <td className="p-2 border-r-2 border-t-2 border-border-color pl-4">$ {((producto.precioUni * 0.13) + (producto.precioUni)).toFixed(2)}</td>  */} {/*precio neto unitario*/}
                                    </>
                                }
                                <td className="p-2 border-r-2 border-t-2 border-border-color pl-4">$ {producto.ventaNoSuj}</td>
                                <td className="p-2 border-r-2 border-t-2 border-border-color pl-4">$ {producto.ventaExenta}</td>
                                <td className="p-2 border-r-2 border-t-2 border-border-color pl-4">$ {producto.ventaGravada}</td>
                                <td className="p-2 border-r-2 border-t-2 border-border-color pl-4">$ 0.00</td>
                                <td className="p-2 border-r-2 border-t-2 border-border-color pl-4">$ 0.00</td>
                            </tr>
                        ))
                    }
                </tbody>
            </table>
        </>
    )
}