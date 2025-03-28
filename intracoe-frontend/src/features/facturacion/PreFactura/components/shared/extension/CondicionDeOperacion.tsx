interface CondicionOperacionProps {
    condicion: number
}

export const CondicionOperacion: React.FC<CondicionOperacionProps> = ({ condicion }) => {
    return (
        <div className="border-2 border-border-color rounded-md text-start py-3 px-4">
            <p><span className="font-bold">Condicion de operación: </span>{condicion}</p>
        </div>
    )
}