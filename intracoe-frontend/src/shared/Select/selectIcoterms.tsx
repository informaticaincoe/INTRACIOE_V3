import { Dropdown } from 'primereact/dropdown';
import { HTMLProps, useEffect, useState } from 'react';
import { getAllIncoterms, getAllTipoDomicilioFiscal } from '../catalogos/services/catalogosServices';

interface SelectIcotermsProps {
    icotermSelecionado: any;
    setIcotermSelecionado: any;
    className?: HTMLProps<HTMLElement>['className'];
}

export const SelectIcotermsComponent: React.FC<SelectIcotermsProps> = ({
    icotermSelecionado,
    setIcotermSelecionado,
    className,
}) => {
    const [icoterm, setIcoterm] = useState<[]>([]);

    useEffect(() => {
        fetchListaIcoterms();
    }, []);

    const fetchListaIcoterms = async () => {
        try {
            const response = await getAllIncoterms();
            console.log(response);
            setIcoterm(response);
        } catch (error) {
            console.log(error);
        }
    };

    return (
        <div className="flex flex-col items-start gap-1">
            <label htmlFor="tipoTransmision" className="opacity-70">
                Icoterms
            </label>
            <Dropdown
                value={icotermSelecionado}
                onChange={(e) =>
                   setIcotermSelecionado(e.value)
                }
                options={icoterm}
                optionLabel="descripcion"
                optionValue="id"
                placeholder="Seleccionar icotem"
                className="md:w-14rem font-display w-full text-start"
            />
        </div>
    );
};
