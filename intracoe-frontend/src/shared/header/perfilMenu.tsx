import { Sidebar } from "primereact/sidebar"
import defaultPerfil from "../../assets/grupo_incoe_logo.png"
import { useState } from "react";
import { password, Perfil } from "../interfaces/interfaces";
import banner from "../../assets/banner.png"
import { Divider } from "primereact/divider";
import { Dialog } from "primereact/dialog";
import { Input } from "../forms/input";
/* icons */
import { RiLockPasswordLine } from "react-icons/ri";
import { IoIosLogOut } from "react-icons/io";
import { MdPerson } from "react-icons/md";
import { HiOutlineStatusOnline } from "react-icons/hi";
import { FaRegClock } from "react-icons/fa6";
import { EditableField } from "./editableFiedl";

interface PerfilMenuProps {
    visible: boolean,
    setVisible: any
}

export const PerfilMenu: React.FC<PerfilMenuProps> = ({ visible, setVisible }) => {
    const [visibleChangePassword, setVisibleChangePassword] = useState(false)
    const [formData, setFormData] = useState<Perfil>({
        usuario: 'admin',
        correo: 'admin@email.com',
    });

    const [firstName, setFirstName] = useState("Nombre")
    const [lastName, setLastName] = useState("Apellido")

    const [formDataPasswordChange, setFormDataPasswordChange] = useState<password>({
        newPassword:'',
        password: '',
        confirmPassword: '',
    });

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleChangePassword = (e: React.ChangeEvent<HTMLInputElement>) => {
        setFormDataPasswordChange({ ...formDataPasswordChange, [e.target.name]: e.target.value });
    };

    return (
        <>
            <Sidebar position="right" visible={visible} onHide={() => setVisible(false)} style={{ width: '20vw' }}>
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
                        <div className="px-5 flex flex-col py-3">
                            {/* Usuario */}
                            <EditableField
                                value={formData.usuario}
                                onSave={(val) => setFormData({ ...formData, usuario: val })}
                                labelClass="text-lg font-bold"
                            />

                            {/* Correo */}
                            <EditableField
                                value={formData.correo}
                                onSave={(val) => setFormData({ ...formData, correo: val })}
                            />

                        </div>

                        <div className="mt-15 px-7 text-sm text-gray-700 space-y-10">
                            {/* Perfil */}
                            <div>
                                <span className="flex items-center gap-2">
                                    <MdPerson size={20} className="opacity-60" />
                                    <p className="font-medium text-gray-800">Perfil</p>
                                </span>
                                <Divider
                                    pt={{
                                        root: {
                                            style: {
                                                margin: '4% 0',
                                                padding: 0
                                            }
                                        }
                                    }}
                                />

                                <div className=" text-gray-600 space-y-1 px-7">
                                    <p>Nombre: {firstName}</p>
                                    <p>Apellido: {lastName}</p>
                                </div>
                            </div>
                            {/* Estado */}
                            <div>
                                <span className="flex items-center gap-2">
                                    <HiOutlineStatusOnline size={22} className="opacity-70" />
                                    <p className="font-medium text-gray-800">Estado</p>
                                </span>
                                <Divider
                                    pt={{
                                        root: {
                                            style: {
                                                margin: '4% 0',
                                                padding: 0
                                            }
                                        }
                                    }}
                                />
                                <div className=" text-green-600 font-medium px-7">● Activo</div>
                            </div>

                            {/* Última conexión */}
                            <div>
                                <span className="flex items-center gap-2">
                                    <FaRegClock size={18} className="opacity-70" />
                                    <p className="font-medium text-gray-800">Última conexión</p>
                                </span>
                                <Divider
                                    pt={{
                                        root: {
                                            style: {
                                                margin: '4% 0',
                                                padding: 0
                                            }
                                        }
                                    }}
                                />
                                <div className="text-gray-600 px-7">2025-04-08 15:12:23</div>
                            </div>
                        </div>

                    </div>

                    {/* Cambio de Contraseña */}
                    <div className="px-7 pb-5">

                        <span className="flex gap-2 items-center" onClick={() => setVisibleChangePassword(true)}>
                            <RiLockPasswordLine />
                            <p className="">Contraseña Anterior</p>
                        </span>
                        <Divider />
                        <span className="flex gap-2 items-center">
                            <IoIosLogOut size={20} />
                            <p className="">Cerrar sesión</p>
                        </span>
                    </div>
                </div>
            </Sidebar>
            {visibleChangePassword &&
                <Dialog header="Cambiar contraseña" visible={visibleChangePassword} modal={false} style={{ width: '35vw' }} onHide={() => { if (!visibleChangePassword) return; setVisibleChangePassword(false); }}>
                    <div className="flex flex-col gap-10 px-5 py-1">

                        <div className="flex flex-col gap-5">
                        <span>
                                <p>Contraseña anterior:</p>
                                <Input name="newPassword" value={formDataPasswordChange.newPassword} onChange={handleChangePassword} />
                            </span>
                            <span>
                                <p>Nueva contraseña:</p>
                                <Input name="password" value={formDataPasswordChange.password} onChange={handleChangePassword} />
                            </span>
                            <span>
                                <p>Confirmar nueva contraseña:</p>
                                <Input name="confirmPassword" value={formDataPasswordChange.confirmPassword} onChange={handleChangePassword} />
                            </span>
                        </div>
                        <button className="bg-primary-blue text-white py-3 rounded-md">Cambiar contraseña</button>
                    </div>
                </Dialog>
            }
        </>
    );
};