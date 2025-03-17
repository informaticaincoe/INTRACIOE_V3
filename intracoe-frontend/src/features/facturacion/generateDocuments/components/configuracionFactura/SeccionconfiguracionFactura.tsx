import React, { useEffect, useState } from 'react'
import { WhiteSectionsPage } from '../../../../../shared/containers/whiteSectionsPage'
import { Divider } from 'antd'
import Dropdown from 'antd/es/dropdown/dropdown'

interface SeccionconfiguracionFacturaInterface {
    tipoDteLista: any;
    setTipoDte: any;
    tipoDte: any;
}

export const SeccionconfiguracionFactura: React.FC<SeccionconfiguracionFacturaInterface> = ({ tipoDteLista, setTipoDte, tipoDte }) => {

      const [tipoDteTempList, setTipoDteTempLista] = useState([]);  // Lista de tipos de documentos
    

    return (
        <WhiteSectionsPage>
            <div className='pt2 pb-5'>
                <h1 className="text-start font-bold text-xl">Configuración factura</h1>
                <Divider className="m-0 p-0"></Divider>
                {tipoDteLista}
                {/* <Dropdown
                    value={tipoDte}  // El valor seleccionado actualmente
                    onChange={(e) => setTipoDte(e.value)}  // Actualiza el estado con el tipo de documento seleccionado
                    options={tipoDteLista}  // Las opciones que vienen del API
                    optionLabel="label"  // Mostrar 'descripcion' de cada opción
                    optionValue="value"  // El valor de la opción es el 'id' de cada tipo de documento
                    placeholder="Seleccionar tipo de documento"
                    className="md:w-14rem font-display w-full"
                /> */}

            </div>
        </WhiteSectionsPage>
    )
}
