import { useState } from "react"
import { Input } from "../../../shared/forms/input"

export const LoginForm = ()=> {

    const [formData, setFormData] = useState({
        username: "",
        password: "",
    });

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    return(
        <form>
            <span className="flex flex-col">
                <label htmlFor="username">Usuario</label>
                <Input name="username" placeholder="usuario" type="text" value={formData.username} onChange={handleChange}/>
            </span>
        </form>
    )
}