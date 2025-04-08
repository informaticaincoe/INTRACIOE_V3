import React from 'react'
import { ReceptorRequestInterface } from '../../../../../shared/interfaces/interfaces';
import { Input } from '../../../../../shared/forms/input';
import { SelectDepartmentComponent } from '../../../../../shared/Select/selectDepartmentComponent';

interface StepperFormInfoContactoReceptorProps {
    formData: ReceptorRequestInterface;
    handleChange: any;
}

export const StepperFormInfoContactoReceptor: React.FC<StepperFormInfoContactoReceptorProps> = ({ formData, handleChange }) => {
    return (
        <div>
            <span>
                <label htmlFor="departamento">Departamentos</label>
            </span>
            <span>
                <label htmlFor="municipio">Municipio</label>
                {/* <SelectDepartmentComponent onChange={handleChange} value={formData.epartamento} name={"departamento"}/> */}
            </span>
            <span>
                <label htmlFor="direccion">Direccion</label>
                <Input onChange={handleChange} value={formData.direccion} name={"direccion"} />
            </span>
            <span>
                <label htmlFor="telefono">Telefono</label>
                <Input onChange={handleChange} value={formData.telefono} name={"telefono"} />
            </span>
            <span>
                <label htmlFor="correo">Correo</label>
                <Input onChange={handleChange} value={formData.correo} name={"correo"} />
            </span>
        </div>
    )
}

