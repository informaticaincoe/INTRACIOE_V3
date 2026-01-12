import { Dropdown } from 'primereact/dropdown';
import { HTMLProps, useEffect, useState } from 'react';
import { getAllTipoDomicilioFiscal } from '../catalogos/services/catalogosServices';

interface SelectTipoDomicilioFiscalProps {
    tipoDomicilioFiscalSelecionado: any;
    setTipoDomicilioFiscalSelecionado: any;
    className?: HTMLProps<HTMLElement>['className'];
}

export const SelectTipoDomicilioFiscalComponent: React.FC<SelectTipoDomicilioFiscalProps> = ({
    tipoDomicilioFiscalSelecionado,
    setTipoDomicilioFiscalSelecionado,
    className,
}) => {
    const [recinto, setRecinto] = useState<[]>([]);

    useEffect(() => {
        fetchListaTipoDomilioFiscal();
    }, []);

    const fetchListaTipoDomilioFiscal = async () => {
        try {
            const response = await getAllTipoDomicilioFiscal();
            console.log(response);
            setRecinto(response);
        } catch (error) {
            console.log(error);
        }
    };

    return (
        <div className="flex flex-col items-start gap-1">
            <label htmlFor="tipoTransmision" className="opacity-70">
                Tipo de domicilio fiscal
            </label>
            <Dropdown
                value={tipoDomicilioFiscalSelecionado}
                onChange={(e) =>
                   setTipoDomicilioFiscalSelecionado(e.value)
                }
                options={recinto}
                optionLabel="descripcion"
                optionValue="id"
                placeholder="Seleccionar recinto"
                className="md:w-14rem font-display w-full text-start"
            />
        </div>
    );
};
