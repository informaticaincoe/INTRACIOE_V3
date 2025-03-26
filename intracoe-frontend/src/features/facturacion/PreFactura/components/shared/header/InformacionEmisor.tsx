import { Emisor } from "../../../interfaces/facturaPdfInterfaces"
import logo from "../../../../../../assets/logo.png"

interface InformacionEmisorProps{
    emisor: Emisor
}

export const InformacionEmisor:React.FC<InformacionEmisorProps> = ({emisor}) => {
    return(
        <div>
            <span>
                <img src={logo} alt="" />
            </span>
            <span>
                <p>{emisor.nombre}</p>
                <p></p>
                <p></p>
                <p></p>
                <p></p>
            </span>
            <span>

            </span>
        </div>
    )
}