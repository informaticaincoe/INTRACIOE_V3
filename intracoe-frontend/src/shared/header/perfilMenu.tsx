import { Sidebar } from "primereact/sidebar"
import defaultPerfil from "../../assets/default-perfil.png"
import { useState } from "react";
import { Perfil } from "../interfaces/interfaces";
import { Input } from "../forms/input";

interface PerfilMenuProps {
    visible: boolean,
    setVisible: any
}

export const PerfilMenu: React.FC<PerfilMenuProps> = ({ visible, setVisible }) => {
    const [formData, setFormData] = useState<Perfil>({
        usuario: '',
        constraseña: '',
        descripcion: '',
    });

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };
    return (
        <Sidebar position="right" visible={visible} onHide={() => setVisible(false)}>
            <img src={defaultPerfil} alt="perfil" className="object-cover px-14 .custom-choose-btn" />
            <h2 className="text-xl font-bold text-center py-3">Admin</h2>

            <div>
                <span>
                    <label htmlFor="usuario">Usuario</label>
                    <Input name="usuario" value={formData.usuario} onChange={ handleChange }/>
                </span>
                <span>
                    <label htmlFor="usuario">Cambiar contaseña</label>
                    <Input name="usuario" value={formData.constraseña} onChange={ handleChange }/>
                </span>
                <span>
                    <label htmlFor="usuario">Descripción</label>
                    <Input name="usuario" value={formData.descripcion} onChange={ handleChange }/>
                </span>
            </div>
        </Sidebar>
    )
}