export const SeccionDocumentosRelacionados = () => {
    return (
        <>
            <div className="py-5">
                <h1 className="uppercase font-bold">Documentos relacionados</h1>
                <table className="table-fixed border w-full border-border-color text-start rounded-md">
                    <thead className="rounded-md">
                        <tr>
                            <td className=" p-2 border-r border-border-color">Tipo de documento:</td>
                            <td className="p-2 border-r border-border-color">N° documento:</td>
                            <td className="p-2">Fecha del documento:</td>
                        </tr>
                    </thead>
                </table>
            </div>
        </>
    )
}