
import { Dropdown } from 'primereact/dropdown';
import React, { useEffect, useState } from 'react'
import { TipoGeneracionDocumento, TipoGeneracionDocumentoInterface } from './TipoGeneracionDocumento';

interface SelectTipoGeneracionDelDocumentoInterface {
    tipoGeneracion: any;
    setTipoGeneracion: any;
}

export const SelectTipoGeneracionDelDocumento: React.FC<SelectTipoGeneracionDelDocumentoInterface> = ({ tipoGeneracion, setTipoGeneracion }) => {
    const [tipoListaGeneracionDocumento, setTipoListaGeneracionDocumento] = useState<TipoGeneracionDocumentoInterface[]>()

    useEffect(() => {
        fetchTipoListaGeneracionDocumento()
    }, [])

    const fetchTipoListaGeneracionDocumento =()=>{
        setTipoListaGeneracionDocumento(TipoGeneracionDocumento)
    }

    return (
        <Dropdown
            value={tipoGeneracion} // El valor seleccionado actualmente (ahora es el id del tipo de documento)
            onChange={(e: { value: any }) => setTipoGeneracion(e.value)} // Actualiza el estado con el tipo de documento seleccionado
            options={tipoListaGeneracionDocumento} // Las opciones que vienen del API
            optionLabel="descripcion" // Mostrar 'descripcion' de cada opción
            optionValue='codigo'
            placeholder="Seleccionar tipo de documento"
            className="md:w-14rem font-display w-full text-start"
        />
    )
}
