// import { useState } from "react";
import { ProductoRequest } from "../../../../../shared/interfaces/interfaces";
import { Input } from "../../../../../shared/forms/input";
import { Checkbox } from "primereact/checkbox";

interface StepperInformacionGeneralProps {
    formData: ProductoRequest;
    handleChange: any;
}

export const StepperFormImpuestoStock: React.FC<
    StepperInformacionGeneralProps
> = ({ formData, handleChange }) => {
    // const [tributo, setTributo] = useState()

    return (
        <>
            <div className='flex flex-col gap-10'>
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
                            value={formData.stock_maximo.toString()}
                            onChange={handleChange}
                        />
                    </span>
                </div>
                <span className='w-full'>
                    <label htmlFor="tipo_documento" className="flex">
                        <span className="text-red pr-1">*</span> Impuestos
                    </label>
                    <Input
                        type="number"
                        name="impuesto"
                        value={formData.impuestos[0]?.toString()}
                        onChange={handleChange}
                    />
                </span>
                <span className='w-full'>
                    <label htmlFor="tipo_documento" className="flex">
                        <span className="text-red pr-1">*</span> Referencia interna
                    </label>
                    <Input
                        type="number"
                        name="referencia_interna"
                        value={formData.referencia_interna ?? ""}
                        onChange={handleChange}
                    />
                </span>
                <span className='w-full'>
                    <label htmlFor="tipo_documento" className="flex">
                        <span className="text-red pr-1">*</span> Tributo
                    </label>
                    <Input
                        type="number"
                        name="tributo"
                        value={formData.tributo.toString()}
                        onChange={handleChange}
                    />
                </span>
                <span className='w-full flex'>
                    <Checkbox
                        onChange={(e) =>
                            handleChange({ target: { name: 'precio_iva', value: e.checked } })
                        }
                        checked={formData.precio_iva}
                    />
                    <label htmlFor="precio_iva" className="flex pl-2">Precio Iva</label>
                </span>
            </div>
        </>
    )
}