interface CondicionOperacionProps {
    condicion: number
}

export const CondicionOperacion: React.FC<CondicionOperacionProps> = ({ condicion }) => {
    return (
        <div className="border border-border-color rounded-md text-start p-2">
            <p><span className="font-bold">Condicion de operación: </span>{condicion}</p>
        </div>
    )
}