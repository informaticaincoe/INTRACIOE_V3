import { Dropdown } from 'primereact/dropdown';
import { HTMLProps, useEffect, useState } from 'react';
import { getAllRecintoFiscal } from '../catalogos/services/catalogosServices';

interface SelectRecintoFiscalProps {
    recintoFiscalSelecionado: any;
    setRecintoFiscalSelecionado: any;
    className?: HTMLProps<HTMLElement>['className'];
}

export const SelectRecintoFiscalComponent: React.FC<SelectRecintoFiscalProps> = ({
    recintoFiscalSelecionado,
    setRecintoFiscalSelecionado,
    className,
}) => {
    const [recintoFiscal, setRecintoFiscal] = useState<[]>([]);

    useEffect(() => {
        fetchListaRecintoFiscal();
    }, []);

    const fetchListaRecintoFiscal = async () => {
        try {
            const response = await getAllRecintoFiscal();
            console.log(response);
            setRecintoFiscal(response);
        } catch (error) {
            console.log(error);
        }
    };

    return (
        <div className="flex flex-col items-start gap-1">
            <label htmlFor="tipoTransmision" className="opacity-70">
                Recinto Fiscal
            </label>
            <Dropdown
                value={recintoFiscalSelecionado}
                onChange={(e) =>
                    setRecintoFiscalSelecionado(e.value)
                }
                options={recintoFiscal}
                optionLabel="descripcion"
                optionValue="id"
                placeholder="Seleccionar recintoFiscal"
                className="md:w-14rem font-display w-full text-start"
            />
        </div>
    );
};
