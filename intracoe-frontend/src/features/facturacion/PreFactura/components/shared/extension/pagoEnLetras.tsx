interface PagoEnLetrasInterfaceProps {
    cantidadAPagar:string
}

export const PagoEnLetras:React.FC<PagoEnLetrasInterfaceProps> = ({cantidadAPagar}) => {
return(
    <div className="border border-border-color rounded-md text-start p-2">
        <p><span className="font-bold">Son: </span>{cantidadAPagar}</p>
    </div>
)
}