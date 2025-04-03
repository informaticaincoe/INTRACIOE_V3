import React, { useState } from 'react';

import { LuSearch } from "react-icons/lu";
import { FaPlus } from "react-icons/fa";

import { Input } from "../../../../shared/forms/input";
import { useNavigate } from 'react-router';


export const TablaProductosHeader = () => {
    const [formData, setFormData] = useState({
        codigo: '',
    });
    const[showProductosModal, setShowProductosModal] = useState<boolean>(false)
    const navigate = useNavigate()


    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const agregarProducto = () => {
        navigate("/productos/nuevo")
    }

    return (
        <span className="flex justify-between items-center">
            <h1 className="text-lg font-bold">Lista productos</h1>
            <div className="flex gap-5">
                <span className="flex items-center border border-border-color rounded-md w-[30vw]">
                    <span className="pl-4">
                        <LuSearch />
                    </span>
                    <Input placeholder={"Buscar producto por codigo"} name={"codigo"} value={formData.codigo} onChange={handleChange} className=" border-0 focus:ring-0 focus:border-ring-0 active:border-0 focus:outline-none focus:border-none" />
                </span>
                <button onClick={agregarProducto} className="flex items-center gap-2 bg-primary-blue text-white px-7 hover:cursor-pointer py-3 rounded-md">
                    <FaPlus size={14} />
                    <span>Agregar producto</span>
                </button>
            </div>
        </span>
    )
}
