import { useState } from "react"
import { Title } from "../../../shared/text/title"
import { TableContainer } from "../../facturacion/activities/components/activitiesTable/tableContainer"

export const CatalogosPage = () => {
  const [showSideMenu, setshowSideMenu] = useState(false)

  return (
    <>
      <Title text="Catalogos" />

        <div className="grid grid-cols-[18%_82%] gap-10 p-10 h-full">
          <div className="text-start bg-white py-5 px-5">
            <h2 className="font-semibold text-xl pb-5">Lista catalogos</h2>
            <div className="h-[1px] w-full bg-gray-200 mb-5"></div>
            <ul className=" h-full flex flex-col gap-2">
              <li onClick={() => setshowSideMenu(!showSideMenu)} className="bg-blue-200 px-2 py-1 rounded-md">Catalogo</li>
              <li className="px-2 py-1">Descuentos</li>
              <li className="px-2 py-1">Ambientes</li>
              <li className="px-2 py-1">Plazos</li>
            </ul>
          </div>
          <div className="justify-center bg-white p-5">
              <TableContainer />

          </div>
        </div>
    </>
  )
}
