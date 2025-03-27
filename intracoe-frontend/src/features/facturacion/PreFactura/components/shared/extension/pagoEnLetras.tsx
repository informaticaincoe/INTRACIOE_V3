interface PagoEnLetrasInterfaceProps {
    cantidadAPagar:string
}

export const PagoEnLetras:React.FC<PagoEnLetrasInterfaceProps> = ({cantidadAPagar}) => {
return(
    <div className="border-2 border-border-color rounded-md text-start py-3 px-4">
        <p><span className="font-bold">Son: </span>{cantidadAPagar}</p>
    </div>
)
}