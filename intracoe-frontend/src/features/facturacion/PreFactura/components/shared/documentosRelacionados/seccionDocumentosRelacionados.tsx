export const SeccionDocumentosRelacionados = () => {
  return (
    <>
      <div className="py-5">
        <h1 className="font-bold uppercase">Documentos relacionados</h1>
        <table className="border-border-color w-full table-fixed rounded-md border-2 text-start">
          <thead className="rounded-md">
            <tr>
              <td className="border-border-color border-r-2 p-2">
                Tipo de documento:
              </td>
              <td className="border-border-color border-r-2 p-2">
                N° documento:
              </td>
              <td className="p-2">Fecha del documento:</td>
            </tr>
          </thead>
        </table>
      </div>
    </>
  );
};
