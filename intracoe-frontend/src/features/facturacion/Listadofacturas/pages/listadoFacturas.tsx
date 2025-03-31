import { WhiteSectionsPage } from "../../../../shared/containers/whiteSectionsPage"
import { Title } from "../../../../shared/text/title"
import { TableListadoFacturasContainer } from "../componentes/TableListadoFacturasContainer"

export const ListadoFActuras = () => {
    return (
        <>
            <Title text='Listado Facturas' />
            <WhiteSectionsPage>
                <>
                <TableListadoFacturasContainer />
                </>
            </WhiteSectionsPage>
        </>
    )
}