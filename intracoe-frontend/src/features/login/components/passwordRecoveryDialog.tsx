// PasswordRecoveryDialog.tsx
import React from 'react';
import { Dialog } from 'primereact/dialog';
import { InputOtp } from 'primereact/inputotp';
import { RiLockPasswordFill } from 'react-icons/ri';
import { Input } from '../../../shared/forms/input';

interface PasswordRecoveryDialogProps {
    visible: boolean;
    step1: boolean;
    codigo: string | number | null | undefined;
    newPassword: string;
    onChangeCodigo: (value: string | number | null | undefined) => void;
    onChangeNewPassword: (value: string) => void;
    onConfirm: () => void;
    onCancel: () => void;
    onNextStep: () => void;
}

export const PasswordRecoveryDialog: React.FC<PasswordRecoveryDialogProps> = ({
    visible,
    step1,
    codigo,
    newPassword,
    onChangeCodigo,
    onChangeNewPassword,
    onConfirm,
    onCancel,
    onNextStep,
}) => {
    return (
        <Dialog visible={visible} style={{ width: '50vw' }} onHide={onCancel}>
            {step1 ? (
                <div>
                    <RiLockPasswordFill size={100} className='text-center w-full pb-5' />
                    <p className='text-xl font-bold text-center'>Codigo de recuperación</p>
                    <label className="m-0 text-center">
                        Codigo de recuperación enviado al correo:
                        <span className='italic'> karen.burgos@grupoincoe.com</span>
                    </label>
                    <div className='pt-5 flex flex-col justify-center items-center'>
                        <label htmlFor="codigo">Codigo de verificacion:</label>
                        <InputOtp name="codigo" value={codigo} onChange={(e) => onChangeCodigo(e.value)} integerOnly length={6} style={{ padding: '3% 0' }} />
                    </div>
                    <div className='flex gap-3 w-full justify-end'>
                        <button className='px-6 py-2 bg-primary-blue text-white rounded-md' onClick={onNextStep}>Confirmar</button>
                        <button className='px-6 py-2 border border-primary-blue text-primary-blue rounded-md' onClick={onCancel}>Cancelar</button>
                    </div>
                </div>
            ) : (
                <div>
                    <RiLockPasswordFill size={100} className='text-center w-full pb-5' />
                    <p className='text-xl font-bold text-center pb-10'>Recuperación de contraseña</p>
                    <label className="m-0 text-center">
                        Ingrese su nueva contraseña
                    </label>
                    <Input name="newPassword" className="mb-5" value={newPassword} onChange={(e) => onChangeNewPassword(e.target.value)} />
                    <div className='flex gap-3 w-full justify-end'>
                        <button className='px-6 py-2 bg-primary-blue text-white rounded-md' onClick={onConfirm}>Confirmar</button>
                        <button className='px-6 py-2 border border-primary-blue text-primary-blue rounded-md' onClick={onCancel}>Cancelar</button>
                    </div>
                </div>
            )}
        </Dialog>
    );
};
