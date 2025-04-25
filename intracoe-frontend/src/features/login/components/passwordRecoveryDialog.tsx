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
    <Dialog visible={visible} style={{ width: '45%' }} onHide={onCancel}>
      {step1 ? (
        <div>
          <RiLockPasswordFill size={100} className="w-full pb-5 text-center" />
          <p className="text-center text-xl font-bold">
            Codigo de recuperación
          </p>
          <p className="m-0 text-center">
            Codigo de recuperación enviado al correo:
            <span className="italic"> karen.burgos@grupoincoe.com</span>
          </p>
          <div className="flex flex-col items-center justify-center pt-5">
            <label htmlFor="codigo">Codigo de verificacion:</label>
            <InputOtp
              name="codigo"
              value={codigo}
              onChange={(e) => onChangeCodigo(e.value)}
              integerOnly
              length={6}
              style={{ padding: '3% 0' }}
            />
          </div>
          <div className="flex w-full justify-end gap-3">
            <button
              className="bg-primary-blue rounded-md px-6 py-2 text-white"
              onClick={onNextStep}
            >
              Confirmar
            </button>
            <button
              className="border-primary-blue text-primary-blue rounded-md border px-6 py-2"
              onClick={onCancel}
            >
              Cancelar
            </button>
          </div>
        </div>
      ) : (
        <div>
          <RiLockPasswordFill size={100} className="w-full pb-5 text-center" />
          <p className="pb-10 text-center text-xl font-bold">
            Recuperación de contraseña
          </p>
          <label className="m-0 text-center">Ingrese su nueva contraseña</label>
          <Input
            name="newPassword"
            className="mb-5"
            value={newPassword}
            onChange={(e) => onChangeNewPassword(e.target.value)}
          />
          <div className="flex w-full justify-end gap-3">
            <button
              className="bg-primary-blue rounded-md px-6 py-2 text-white"
              onClick={onConfirm}
            >
              Confirmar
            </button>
            <button
              className="border-primary-blue text-primary-blue rounded-md border px-6 py-2"
              onClick={onCancel}
            >
              Cancelar
            </button>
          </div>
        </div>
      )}
    </Dialog>
  );
};
