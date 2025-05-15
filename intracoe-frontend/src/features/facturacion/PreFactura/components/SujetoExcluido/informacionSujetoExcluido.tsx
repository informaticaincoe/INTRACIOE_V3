import React, { useEffect, useState } from 'react'
import { tipoIdReceptor } from '../../../../../shared/services/receptor/receptorServices';
import { SujetoExcluido } from '../../interfaces/sujetoExcluidoInterfaces';
import { TipoIdentificacion } from '../../interfaces/facturaPdfInterfaces';

interface InformacionSujetoExcluidoProp {
    sujetoExcluido: SujetoExcluido;
}

export const InformacionsujetoExcluido: React.FC<InformacionSujetoExcluidoProp> = ({
    sujetoExcluido,
}) => {
    const [tipoIdDocumento, setTipoDocumento] =
        useState<TipoIdentificacion | null>(null);

    useEffect(() => {
        if (sujetoExcluido.tipoDocumento) {
            fetchTipoID();
        }
    }, [sujetoExcluido.tipoDocumento]);

    const fetchTipoID = async () => {
        if (sujetoExcluido.tipoDocumento) {
            try {
                const aux = await tipoIdReceptor(sujetoExcluido.tipoDocumento);
                setTipoDocumento(aux);
            } catch (error) {
                console.log(error);
            }
        }
    };
    return (
        <div className="pt-8">
            <h1 className="font-bold uppercase">Sujeto Excluido</h1>
            <div className="border-border-color grid grid-cols-[auto_1fr] gap-x-5 rounded-md border-2 p-5 text-start">
                <div className="flex flex-col gap-1.5 opacity-70">
                    <p>Nombre o razon social:</p>
                    <p>Actividad economica:</p>
                    <p>Documento identificacion:</p>
                    <p>Correo electronico:</p>
                    <p>telefono:</p>
                    <p>direccion:</p>
                </div>
                <div className="flex flex-col gap-1.5">
                    <p>{sujetoExcluido.nombre}</p>
                    {sujetoExcluido.numDocumento && (
                        <p>
                            {tipoIdDocumento?.descripcion} - {sujetoExcluido.numDocumento}
                        </p>
                    )}
                    <p>{sujetoExcluido.codActividad} - {sujetoExcluido.descActividad}</p>
                    <p>{sujetoExcluido.correo}</p>
                    <p>{sujetoExcluido.telefono}</p>
                    <p>{sujetoExcluido.direccion.complemento}</p>
                </div>
            </div>
        </div>
    );
};
