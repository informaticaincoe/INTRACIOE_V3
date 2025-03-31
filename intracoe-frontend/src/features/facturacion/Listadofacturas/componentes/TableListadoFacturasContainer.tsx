import React, { useEffect, useState } from 'react'
import { getAllFacturas } from '../services/listadoFacturasServices'
import { FacturaListado, ListResult } from '../../../../shared/interfaces/interfaceFacturaJSON'

export const TableListadoFacturasContainer = () => {
    const [data, setData] = useState<ListResult[]>([])

    useEffect(() => {
        fetchFacturas()
    }, [])

    const fetchFacturas = async () => {
        try {
            const response = await getAllFacturas()
            setData(response.results)
            console.log("response.results", response.results)
        } catch (error) {
            console.log(error)
        }
    }

    return (
        <div>
            {
                // Map through the data to render the list of elements
                data && data.map(element => (
                    <p key={element.id}>{element.id}</p> // Render each element with its id
                ))
            }
        </div>
    )
}
