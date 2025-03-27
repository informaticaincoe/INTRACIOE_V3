import { Extension } from "../../../interfaces/facturaPdfInterfaces"

interface ExtensionInterfaceProps {
    extension: Extension
}

export const SeccionExtension: React.FC<ExtensionInterfaceProps> = ({ extension }) => {
    return (

        <div className="flex flex-col gap-8 h-full">
            
            <div className="border-2 border-border-color rounded-md text-start py-3 px-4 h-full grid grid-rows-2">
                <div className="grid grid-cols-[70%_30%] justify-between ">
                    <p><span className="font-bold">Responsable por parte del emisor: </span>{extension.nombEntrega}</p>
                    <p><span className="font-bold ">N° de documento: </span>{extension.nombEntrega}</p>
                </div>
                <div className="grid grid-cols-[70%_30%] justify-between ">
                    <p><span className="font-bold">Responsable por parte del receptor</span>{extension.nombEntrega}</p>
                    <p><span className="font-bold ">N° de documento: </span>{extension.nombEntrega}</p>
                </div>
            </div>
        </div>
    )
}