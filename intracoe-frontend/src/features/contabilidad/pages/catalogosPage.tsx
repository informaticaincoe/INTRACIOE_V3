import { useState } from "react"
import { WhiteSectionsPage } from "../../../shared/containers/whiteSectionsPage"
import { Title } from "../../../shared/text/title"
import { ActivitiesPage } from "../../facturacion/activities/pages/activitiesPage"
import { TableContainer } from "../../facturacion/activities/components/activitiesTable/tableContainer"

export const CatalogosPage = () => {
  const [showSideMenu, setshowSideMenu] = useState(false)

  return (
    <>
      <Title text="Catalogos" />

        <div className="grid grid-cols-[15%_85%] gap-10 p-10 h-full">
          <div className="text-start bg-white py-5 px-5">
            <h2 className="font-semibold text-xl pb-5">Lista catalogos</h2>
            <ul className=" h-full flex flex-col gap-5">
              <li onClick={() => setshowSideMenu(!showSideMenu)} className="bg-blue-200 p-2 rounded-md">Catalogo</li>
              <li className="px-2">Descuentos</li>
              <li className="px-2">Ambientes</li>
              <li className="px-2">Plazos</li>
            </ul>
          </div>
          <div className="justify-center bg-white p-5">
              <TableContainer />
          </div>
        </div>
    </>
  )
}
