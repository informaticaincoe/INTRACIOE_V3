
import React, { useRef, useState } from "react";
import { Button } from 'primereact/button';
import { Dialog } from 'primereact/dialog';
import { FaCheckCircle } from "react-icons/fa";
import { IoMdCloseCircle } from "react-icons/io";
import { addProveedor } from "../../../../../ventas/proveedores/services/proveedoresServices";
import CustomToast, { CustomToastRef, ToastSeverity } from "../../../../../../shared/toast/customToast";
import { ProveedorResultInterface } from "../../../../../ventas/proveedores/interfaces/proveedoresInterfaces";
import { Input } from "../../../../../../shared/forms/input";

interface ModalSujetoExcluidosProps {
    visible: boolean,
    setVisible: any
    update:any
}

export const ModalSujetoExcluidos: React.FC<ModalSujetoExcluidosProps> = ({ visible, setVisible, update }) => {
    const toastRef = useRef<CustomToastRef>(null);
    const [formData, setFormData] = useState<ProveedorResultInterface>({
        id: 0,
        nombre: '',
        ruc_nit: '',
        contacto: null,
        telefono: null,
        email: null,
        direccion: null,
        condiciones_pago: null,
    });

    const handleAccion = (
        severity: ToastSeverity,
        icon: any,
        summary: string
    ) => {
        toastRef.current?.show({
            severity: severity,
            summary: summary,
            icon: icon,
            life: 2000,
        });
    };



    const handleChange = (e: any) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSendForm = async () => {

        try {
            const response = await addProveedor(formData);
            console.log(response);
            handleAccion(
                'success',
                <FaCheckCircle size={38} />,
                'proveedor creado con exito'
            );

            setTimeout(() => {
                update()
                setVisible(false);
            }, 2000);
        } catch (error) {
            handleAccion(
                'error',
                <IoMdCloseCircle size={38} />,
                'Error al crear el proveedor'
            );
        }

    };
    return (
        <div className="card flex justify-content-center">
            <Dialog header={<p className="px-5">Agregar proveedor</p>} visible={visible} modal={true} style={{ width: '50vw' }} onHide={() => { if (!visible) return; setVisible(false); }}>
                <div className="absolute z-20">
                    <CustomToast ref={toastRef} />
                </div>
                
                <div className="rounded-md bg-white p-5">
                    <div>
                        <form action="" className="flex flex-col gap-6 text-start">
                            <span>
                                <label htmlFor="">Nombre</label>
                                <Input
                                    name="nombre"
                                    value={formData.nombre}
                                    onChange={handleChange}
                                />
                            </span>
                            <span>
                                <label htmlFor="">NIT o RUC</label>
                                <Input
                                    name="ruc_nit"
                                    value={formData.ruc_nit}
                                    onChange={handleChange}
                                />
                            </span>
                            <span>
                                <label htmlFor="">Contacto</label>
                                <Input
                                    name="contacto"
                                    value={formData.contacto ?? ''}
                                    onChange={handleChange}
                                />
                            </span>
                            <span>
                                <label htmlFor="">Telefono</label>
                                <Input
                                    name="telefono"
                                    value={formData.telefono ?? ''}
                                    onChange={handleChange}
                                />
                            </span>
                            <span>
                                <label htmlFor="">Correo</label>
                                <Input
                                    name="email"
                                    value={formData.email ?? ''}
                                    onChange={handleChange}
                                />
                            </span>
                            <span>
                                <label htmlFor="">Direccion</label>
                                <Input
                                    name="direccion"
                                    value={formData.direccion ?? ''}
                                    onChange={handleChange}
                                />
                            </span>
                            <span>
                                <label htmlFor="">Condiciones de pago</label>
                                <Input
                                    name="condiciones_pago"
                                    value={formData.condiciones_pago ?? ''}
                                    onChange={handleChange}
                                />
                            </span>
                        </form>
                        <div className="flex w-full justify-start pt-5">
                            <button
                                className="bg-primary-blue rounded-md px-7 py-2 text-white"
                                onClick={handleSendForm}
                            >
                                Guardar
                            </button>
                        </div>
                    </div>
                </div>
            </Dialog>
        </div>
    )
}
