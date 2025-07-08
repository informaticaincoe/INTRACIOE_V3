import React from 'react'
import { Input } from '../../../../../../../shared/forms/input'

interface MotivoContingenciaProps {
    motivo: string,
    setMotivo: any
}

export const MotivoContingencia: React.FC<MotivoContingenciaProps> = ({ motivo, setMotivo }) => {
    return (
        <div className="flex flex-col items-start gap-1">
            <label className="opacity-70">
                Modelo de facturación
            </label>
            <Input name={'motivo'} value={motivo} onChange={(e:any)=> setMotivo(e.value)} />
        </div>
    )
}
