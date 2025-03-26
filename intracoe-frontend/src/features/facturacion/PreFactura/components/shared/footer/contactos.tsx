import { Emisor } from "../../../interfaces/facturaPdfInterfaces"
import { TfiEmail } from "react-icons/tfi";
import { BsTelephone } from "react-icons/bs";

interface ContactosProps {
    emisor: Emisor
}

export const Contactos: React.FC<ContactosProps> = ({ emisor }) => {
    return (
        <div className="w-full flex justify-end gap-10 pt-5">
            <p>Contactanos:</p>
            <span className="flex gap-4">
                <TfiEmail />
                <p>{emisor.correo}</p>
            </span>
            <span className="flex gap-4">
                <BsTelephone />
                <p>Tel. {emisor.telefono}</p>
            </span>
        </div>
    )
}