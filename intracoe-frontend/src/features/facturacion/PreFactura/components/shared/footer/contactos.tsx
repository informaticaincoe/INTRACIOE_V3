import { Emisor } from "../../../interfaces/facturaPdfInterfaces"
import { TfiEmail } from "react-icons/tfi";
import { BsTelephone } from "react-icons/bs";

interface ContactosProps {
    emisor: Emisor
}

export const Contactos: React.FC<ContactosProps> = ({ emisor }) => {
    return (
        <div className="w-full flex justify-end gap-10 pt-3">
            <p>Contactanos:</p>
            <span className="flex gap-2 justify-center items-center">
                <TfiEmail />
                <p>{emisor.correo}</p>
            </span>
            <span className="flex gap-2 justify-center items-center">
                <BsTelephone />
                <p>Tel. {emisor.telefono}</p>
            </span>
        </div>
    )
}