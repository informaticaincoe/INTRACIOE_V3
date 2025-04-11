import React from 'react'
import { HeaderTable } from '../../facturacion/activities/components/headerTable/headerTable'


interface TablaCatalogosProp {
    setActivities: any,
    filterTerm: string,
    setFilterTerm: any
}
export const TablaCatalogos: React.FC<TablaCatalogosProp> = ({ setActivities, filterTerm, setFilterTerm }) => {
    return (
        <>
            <div>TablaCatalogos</div>
            <HeaderTable
                filterTerm={filterTerm}
                setFilterTerm={setFilterTerm}
            />
            
        </>
    )
}
