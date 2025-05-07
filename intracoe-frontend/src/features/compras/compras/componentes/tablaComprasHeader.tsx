import React, { useState } from 'react'
import { FaPlus } from 'react-icons/fa6';
import { LuSearch } from 'react-icons/lu';
import { useNavigate } from 'react-router';

interface TablaComprasHeaderProps {
    codigo: string;
    onSearch: (codigo: string) => void;
}

export const TablaComprasHeader: React.FC<TablaComprasHeaderProps> = ({ codigo, onSearch }) => {
    const [input, setInput] = useState<string>(codigo);
    const navigate = useNavigate();

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setInput(e.target.value);
    };

    const handleKeyPress = (e: React.KeyboardEvent) => {
        console.log(e.target);
        // Si el usuario pulsa Enter, ejecuta la búsqueda
        onSearch(input);
    };

    const agregarCompra = () => {
        navigate('/compras/nuevo');
    };

    return (
        <span className="flex items-center justify-between">
            <h1 className="text-lg font-bold">Lista Compras</h1>
            <div className="flex gap-5">
                <span className="border-border-color flex w-[30vw] items-center rounded-md border">
                    <span className="flex pl-4">
                        <LuSearch />
                    </span>
                    <input
                        name="codigo"
                        value={input}
                        onChange={handleChange}
                        onKeyDown={handleKeyPress}
                        className="focus:border-ring-0 w-full border-0 pl-3 focus:border-none focus:ring-0 focus:outline-none active:border-0"
                    />
                </span>
                <button
                    onClick={agregarCompra}
                    className="bg-primary-blue flex items-center gap-2 rounded-md px-7 py-3 text-white hover:cursor-pointer"
                >
                    <FaPlus size={14} />
                    <span>Agregar compra</span>
                </button>
            </div>
        </span>
    );
};
