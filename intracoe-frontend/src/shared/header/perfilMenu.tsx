import { Sidebar } from "primereact/sidebar"
import defaultPerfil from "../../assets/default-perfil.png"
import { useState } from "react";
import { password, Perfil } from "../interfaces/interfaces";
import { Inplace, InplaceContent, InplaceDisplay } from "primereact/inplace";
import { InputText } from "primereact/inputtext";
import { Button } from "primereact/button";
import banner from "../../assets/banner.png"

import { CiEdit } from "react-icons/ci";
import { RiLockPasswordLine } from "react-icons/ri";
import { IoIosLogOut } from "react-icons/io";

import { Divider } from "primereact/divider";
import { Dialog } from "primereact/dialog";
import { Input } from "../forms/input";

interface PerfilMenuProps {
    visible: boolean,
    setVisible: any
}

export const PerfilMenu: React.FC<PerfilMenuProps> = ({ visible, setVisible }) => {
    const [visibleChangePassword, setVisibleChangePassword] = useState(false)
    const [formData, setFormData] = useState<Perfil>({
        usuario: 'admin',
        correo: 'admin@email.com',
        descripcion: 'administrador encargado de gestionar y mantener el sistema',
    });

    const [formDataPasswordChange, setFormDataPasswordChange] = useState<password>({
        password: '',
        confirmPassword: '',
    });

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleChangePassword = (e: React.ChangeEvent<HTMLInputElement>) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    return (
        <>
            <Sidebar position="right" visible={visible} onHide={() => setVisible(false)}>
                <div className="flex flex-col justify-between h-full">
                    <div>
                        <div className="relative w-full flex flex-col items-center mb-10">
                            {/* Banner de fondo */}
                            <img src={banner} className="w-full h-30 bg-blue-200" />

                            {/* Imagen de perfil */}
                            <div className="absolute top-10">
                                <img
                                    src={defaultPerfil}
                                    alt="perfil"
                                    className="w-30 h-30 rounded-full border-4 border-white shadow-md object-cover"
                                />
                            </div>
                        </div>


                        {/* Sección Usuario */}
                        <div className="px-5">
                            <Inplace closable>
                                <InplaceDisplay>
                                    <div className="flex items-center justify-center gap-2">
                                        <p className="text-lg font-bold text-center">{formData.usuario}</p>
                                        <CiEdit className="" size={20} />
                                    </div>
                                </InplaceDisplay>
                                <InplaceContent>
                                    <InputText value={formData.usuario} onChange={handleChange} name="usuario" autoFocus />
                                </InplaceContent>
                            </Inplace>

                            {/* Sección Correo */}
                            <Inplace closable>
                                <InplaceDisplay>
                                    <div className="flex items-center justify-center">
                                        <p className="text-md text-center">{formData.correo}</p>
                                        <CiEdit className="" size={20} />
                                    </div>
                                </InplaceDisplay>
                                <InplaceContent>
                                    <InputText value={formData.correo} onChange={handleChange} name="correo" autoFocus />
                                </InplaceContent>
                            </Inplace>

                            {/* Sección Descripción */}
                            <div className="mt-10 flex text-center w-full">
                                <Inplace closable>
                                    <InplaceDisplay>
                                        <div className="flex items-center">
                                            <p>{formData.descripcion}</p>
                                        </div>
                                    </InplaceDisplay>
                                    <InplaceContent>
                                        <InputText value={formData.descripcion} onChange={handleChange} name="descripcion" autoFocus />
                                    </InplaceContent>
                                </Inplace>
                            </div>
                        </div>
                    </div>

                    {/* Cambio de Contraseña */}
                    <div className="px-5 pb-5">

                        <span className="flex gap-2 items-center" onClick={() => setVisibleChangePassword(true)}>
                            <RiLockPasswordLine />
                            <p className="">Cambiar contraseña</p>
                        </span>
                        <Divider className="pt-0 mt-0"></Divider>
                        <span className="flex gap-2 items-center">
                            <IoIosLogOut size={20} />
                            <p className="">Cerrar sesión</p>
                        </span>

                    </div>
                </div>
            </Sidebar>
            {visibleChangePassword &&
                <Dialog header="Cambiar contraseña" visible={visibleChangePassword} modal={false} style={{ width: '50vw' }} onHide={() => { if (!visibleChangePassword) return; setVisibleChangePassword(false); }}>
                    <div className="flex flex-col gap-10">
                        <div className="flex flex-col gap-5">
                            <span>
                                <p>Nueva contraseña:</p>
                                <Input name="password" value={formDataPasswordChange.password} onChange={handleChangePassword}/>
                            </span>
                            <span>
                                <p>Confirmar nueva contraseña:</p>
                                <Input name="confirmPassword" value={formDataPasswordChange.confirmPassword} onChange={handleChangePassword}/>
                            </span>
                        </div>
                        <button className="bg-primary-blue text-white py-3 rounded-md">Cambiar contraseña</button>
                    </div>
                </Dialog>
            }
        </>
    );
};