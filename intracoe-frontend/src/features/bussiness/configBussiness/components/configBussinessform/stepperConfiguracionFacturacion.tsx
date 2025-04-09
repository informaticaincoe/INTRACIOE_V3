import React, { useEffect } from 'react'
import { RequestEmpresa } from '../../../../../shared/interfaces/interfaces'
import { Input } from '../../../../../shared/forms/input';
import { SelectTipoIdDocumento } from '../../../../../shared/Select/selectTipoIdDocumento';
import { SelectActividadesEconomicas } from '../../../../../shared/Select/selectActividadesEconomicas';
import { SelectAmbienteComponent } from '../../../../../shared/Select/selectAmbienteComponent';
import { SelectTipoEstablecimiento } from '../../../../../shared/Select/selectTipoEstablecimiento';

interface StepperConfiguracionFacturacionProp {
    formData: RequestEmpresa;
    handleChange: any
}

export const StepperConfiguracionFacturacion: React.FC<StepperConfiguracionFacturacionProp> = ({ formData, handleChange }) => {

    useEffect(()=> {
        console.log("ttttttttttttt",formData.tipo_documento)
    })
    return (
        <div className='flex flex-col gap-10 text-start'>
            <span>
                <label htmlFor="tipo_documento">Tipo de documento de identificación:</label>
                <SelectTipoIdDocumento onChange={handleChange} value={formData.tipo_documento} name={"tipo_documento"} />
            </span>
            <span>
                <label htmlFor="nit">Número de documento de identificación:</label>
                <Input onChange={handleChange} value={formData.nit} name={"nit"} />
            </span>
            <span>
                <label htmlFor="nrc">NRC:</label>
                <Input onChange={handleChange} value={formData.nrc} name={"nrc"} />
            </span>
            <span>
                <label htmlFor="nombre_comercial">Nombre comercial:</label>
                <Input onChange={handleChange} value={formData.nombre_comercial} name={"nombre_comercial"} />
            </span>
            <span>
                <label htmlFor="nombre_razon_social">Nombre o razón social:</label>
                <Input onChange={handleChange} value={formData.nombre_razon_social} name={"nombre_razon_social"} />
            </span>
            <span>
                <label htmlFor="ambiente">Ambiente:</label>
                <SelectAmbienteComponent onChange={handleChange} value={formData.ambiente} name={"ambiente"} />
            </span>
            <span>
                <label htmlFor="codigo_punto_venta">Código punto de venta:</label>
                <Input onChange={handleChange} value={formData.codigo_punto_venta} name={"codigo_punto_venta"} />
            </span>
            <span>
                <label htmlFor="codigo_establecimiento">Código de establecimiento:</label>
                <Input onChange={handleChange} value={formData.codigo_establecimiento} name={"codigo_establecimiento"} />
            </span>
            <span>
                <label htmlFor="actividades_economicas"> Actividad economica </label>
                <SelectActividadesEconomicas onChange={handleChange} value={formData.actividades_economicas ?? ""} name={"actividades_economicas"} />
            </span>
            <span>
                <label htmlFor="tipoestablecimiento">Tipo establecimiento:</label>
                <SelectTipoEstablecimiento onChange={handleChange} value={formData.tipoestablecimiento} name={"tipoestablecimiento"} />
            </span>
            <span>
                <label htmlFor="clave_privada">clave_privada:</label>
                <Input onChange={handleChange} value={formData.clave_privada} name={"clave_privada"} />
            </span>
            <span>
                <label htmlFor="email">Clave publica:</label>
                <Input onChange={handleChange} value={formData.clave_publica} name={"clave_publica"} />
            </span>
        </div>
    )
}
