import { useState } from "react";
import { ProductoRequest } from "../../../../../shared/interfaces/interfaces";
import { Input } from "../../../../../shared/forms/input";

interface StepperInformacionGeneralProps {
    formData: ProductoRequest;
    handleChange: any;
}

export const StepperFormImpuestoStock: React.FC<
    StepperInformacionGeneralProps
> = ({ formData, handleChange }) => {
    const [tributo, setTributo] = useState()

    return (
        <>
            <div className='flex flex-col gap-5'>
                <div className='flex w-full gap-5'>
                    <span className='w-full'>
                        <label htmlFor="tipo_documento" className="flex">
                            <span className="text-red pr-1">*</span> Stock:
                        </label>
                        <Input
                            type="number"
                            name="stock"
                            value={formData.stock.toString()}
                            onChange={handleChange}
                        />
                    </span>
                    <span className='w-full'>
                        <label htmlFor="tipo_documento" className="flex">
                            <span className="text-red pr-1">*</span> Stock minimo:
                        </label>
                        <Input
                            type="number"
                            name="stock_minimo"
                            value={formData.stock_minimo.toString()}
                            onChange={handleChange}
                        />
                    </span>
                    <span className='w-full'>
                        <label htmlFor="tipo_documento" className="flex">
                            <span className="text-red pr-1">*</span> Stock maximo
                        </label>
                        <Input
                            type="number"
                            name="stock_maximo"
                            value={formData.descripcion}
                            onChange={handleChange}
                        />
                    </span>
                </div>
            </div>
        </>
    )
}
