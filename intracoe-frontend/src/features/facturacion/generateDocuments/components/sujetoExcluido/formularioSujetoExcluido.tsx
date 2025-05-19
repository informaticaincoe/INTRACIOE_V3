import React, { useEffect, useState } from 'react'
import { Input } from '../../../../../shared/forms/input'
import { SelectTipoIdDocumento } from '../../../../../shared/Select/selectTipoIdDocumento'
import { getMunicipiosById } from '../../../../bussiness/configBussiness/services/ubicacionService'
import { SelectDepartmentComponent } from '../../../../../shared/Select/selectDepartmentComponent'
import { SelectMunicipios } from '../../../../../shared/Select/selectMunicipios'

interface FormularioSujetoExcluidoProps {
    formData: any;
    handleChange: any;
}

export const FormularioSujetoExcluido: React.FC<
    FormularioSujetoExcluidoProps
> = ({ formData, handleChange }) => {
    const [departamentoSelect, setDepartamentoSelect] = useState<string>();

    useEffect(() => {
        if (formData.municipio) fetchDepartamento(); //obtener departamento por medio del municipio cuando se vaya a editar
    }, []);

    const fetchDepartamento = async () => {
        try {
            const response = await getMunicipiosById(formData.municipio.id);
            console.log('Departamento', response);
            setDepartamentoSelect(response.departamento);
        } catch (error) {
            console.log(error);
        }
    };

    return (
        <form className='grid grid-cols-[auto_1fr] gap-5 rounded-md p-5'>
            <span className='flex flex-col text-start '>
                <h3 className='opacity-40 uppercase font-semibold text-sm'>Identificación</h3>
            </span>
            <div className='flex'>
                <div className='w-0.5 h-full bg-gray-100'></div>
                <div className='px-5 w-full flex flex-col gap-4'>
                    <span className=' flex flex-col justify-start items-start w-full'>
                        <label htmlFor="">Tipo de documento</label>
                        <SelectTipoIdDocumento onChange={handleChange} value={"tipoDocumento"} name={"tipoDocumento"} />
                    </span>
                    <span className='flex flex-col justify-start items-start'>
                        <label htmlFor="">Número de identificación</label>
                        <Input name='numDocumento' value={''} onChange={handleChange} />
                    </span>
                    <span className='flex flex-col justify-start items-start col-span-2'>
                        <label htmlFor="">Nombre o razón social </label>
                        <Input name='nombre' value={''} onChange={handleChange} />
                    </span>
                    <span className='flex flex-col justify-start items-start'>
                        <label htmlFor="">Codigo actividad economica</label>
                        <Input name='codActividad' value={''} onChange={handleChange} />
                    </span>
                    <span className='flex flex-col justify-start items-start'>
                        <label htmlFor="">Descripción actividad economica</label>
                        <Input name='descActividad' value={''} onChange={handleChange} />
                    </span>
                </div>
            </div>
            <span className='flex flex-col text-start pt-8'>
                <h3 className='opacity-40 uppercase font-semibold text-sm'>Dirección</h3>
            </span>
            <div className='flex pt-8'>
                <div className='w-0.5 h-ful bg-gray-100'></div>
                <div className='px-5 w-full flex flex-col gap-4'>
                    <span>
                        <label htmlFor="departamento" className='flex flex-col justify-start items-start'>Departamentos</label>
                        <SelectDepartmentComponent
                            setDepartamentoSelect={setDepartamentoSelect}
                            departamentoSelect={departamentoSelect}
                        />
                    </span>
                    <span>
                        <label htmlFor="municipio" className='flex flex-col justify-start items-start'>Municipio</label>
                        <SelectMunicipios
                            onChange={handleChange}
                            department={departamentoSelect}
                            value={formData.municipio}
                            name={'municipio'}
                        />
                    </span>
                    <span className='flex flex-col justify-start items-start col-span-2'>
                        <label htmlFor="">Dirección</label>
                        <Input name='direccion' value={'direccion'} onChange={handleChange} />
                    </span>
                </div>
            </div>
            <span className='flex flex-col text-start pt-8'>
                <h3 className='opacity-40 uppercase font-semibold text-sm'>Contactos</h3>
            </span>
            <div className='flex pt-8'>
                <div className='w-0.5 h-full bg-gray-100'></div>
                <div className='px-5 w-full flex flex-col gap-4'>
                    <span className='flex flex-col justify-start items-start'>
                        <label htmlFor="">Teléfono</label>
                        <Input name='telefono' value={'telefono'} onChange={handleChange} />
                    </span>
                    <span className='flex flex-col justify-start items-start'>
                        <label htmlFor="">Correo</label>
                        <Input name='correo' value={'correo'} onChange={handleChange} />
                    </span>
                </div>
            </div>
        </form>

    )
}
