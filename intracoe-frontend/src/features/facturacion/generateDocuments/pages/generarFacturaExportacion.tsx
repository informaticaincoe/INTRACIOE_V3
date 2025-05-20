import React, { useState } from 'react'
import { WhiteSectionsPage } from '../../../../shared/containers/whiteSectionsPage'
import { Divider } from 'antd'
import { SelectModeloFactura } from '../components/Shared/configuracionFactura/modeloDeFacturacion/selectModeloFactura'
import { SelectTipoTransmision } from '../components/Shared/configuracionFactura/tipoTransmision/selectTipoTransmisión'
import { CheckBoxVentaTerceros } from '../components/Shared/configuracionFactura/ventaTerceros/checkboxVentaTerceros'
import { generarExportacionService, generarSujetoExcluidoService } from '../services/factura/facturaServices'
import { SelectTipoContingencia } from '../components/Shared/configuracionFactura/generacionEnContingencia/selectTipoContingencia'
import { MotivoContingencia } from '../components/Shared/configuracionFactura/generacionEnContingencia/motivoContingencia'

interface GenerarFacturaExportacionProps {
    tipoDocumentoSelected: any
    codigoGeneracion: any
    numeroControl: any
    condicionesOperacionList: any
    descuentosList: any
    tipoContibuyente: string
}

export const GenerarFacturaExportacion: React.FC<GenerarFacturaExportacionProps> = ({
    tipoDocumentoSelected,
    codigoGeneracion,
    numeroControl,
    condicionesOperacionList,
    descuentosList,
    tipoContibuyente,
}) => {
    const [tipoTransmision, setTipoTransmision] = useState<string>('');
    const [tipoModeloFacturacionSeleccionado, setTipoModeloFacturacionSeleccionado] = useState<any[]>([]); // TODO: Guardar el tipo de modelo
    const [tipoContingencia, setTipoContingencia] = useState<any>()
    const [motivo, setMotivo] = useState<string>('')

    /*************** Generar documento ***************/

    const handleClickGenerarFactura = async () => {

        const dataExportacion = {
            tipo_transmision_codigo: tipoTransmision,
            modelo_facturacion_codigo: tipoModeloFacturacionSeleccionado,
            tipo_contingencia_codigo: tipoContingencia,
            motivo:motivo
        };

        console.log(dataExportacion);

        // try {
        //     const response = await generarSujetoExcluidoService(dataExportacion);
        //     firmarFactura(response.factura_id);
        // } catch (error) {
        //     console.log(error);
        // }
    };

    /*************************************************/

    console.log(tipoDocumentoSelected)
    return (
        <WhiteSectionsPage>
            <div className="pt2 pb-5">
                <h1 className="text-start text-xl font-bold">
                    Configuración factura
                </h1>
                <Divider className="m-0 p-0"></Divider>
                <div className="flex flex-col gap-8">
                    <SelectModeloFactura
                        tipoModeloFacturacionSeleccionado={tipoModeloFacturacionSeleccionado}
                        setTipoModeloFacturacionSeleccionado={setTipoModeloFacturacionSeleccionado}
                    />
                    <SelectTipoTransmision
                        setTipoTransmision={setTipoTransmision}
                        tipoTransmision={tipoTransmision}
                    />

                    {tipoTransmision == '2' &&
                        <SelectTipoContingencia
                            setTipoContingencia={setTipoContingencia}
                            tipoContingencia={tipoContingencia}
                        />
                    }

                    {tipoContingencia == 5 &&
                        <MotivoContingencia
                            setMotivo={setMotivo}
                            motivo={motivo}
                        />

                    }

                    <CheckBoxVentaTerceros />
                </div>
                <div className="mx-14 flex">
                    <button
                        type="button"
                        className="bg-primary-yellow mb-5 self-start rounded-md px-5 py-3 text-white hover:cursor-pointer"
                        onClick={handleClickGenerarFactura}
                    >
                        Generar factura
                    </button>
                </div>
            </div>
        </WhiteSectionsPage>
    )
}
