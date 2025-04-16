import { Dropdown } from 'primereact/dropdown';
import { HTMLProps, useEffect, useState } from 'react';
import { getAllPaises } from '../catalogos/services/catalogosServices';

interface SelectPaisProps {
    value: any;
    onChange: any;
    className?: HTMLProps<HTMLElement>['className'];
    name: string;
}

export const SelectPaisComponent: React.FC<SelectPaisProps> = ({
    value,
    onChange,
    className,
    name,
}) => {
    const [pais, setPais] = useState<[]>([]);

    useEffect(() => {
        fetchListapais();
    }, []);

    const fetchListapais = async () => {
        try {
            const response = await getAllPaises();
            console.log(response);
            setPais(response);
        } catch (error) {
            console.log(error);
        }
    };

    return (
        <div className="justify-content-center flex">
            <Dropdown
                value={value}
                onChange={(e) =>
                    onChange({
                        target: {
                            name,
                            value: e.value,
                        },
                    })
                }
                options={pais}
                optionLabel="descripcion"
                optionValue="id"
                placeholder="Seleccionar pais"
                className="md:w-14rem font-display w-full"
            />
        </div>
    );
};
