import { useState } from 'react';
import { Input } from '../../../shared/forms/input';
import { SendFormButton } from '../../../shared/buttons/sendFormButton';
import { useNavigate } from 'react-router';

export const LoginForm = () => {
  const navigate = useNavigate(); // Hook para navegar en React Router

  const [formData, setFormData] = useState({
    username: '',
    password: '',
  });
  // const [error, setError] = useState<string | null>(null);
  const [errors, setErrors] = useState({
    username: '',
    password: '',
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handlerForm = (e: React.FormEvent) => {
    e.preventDefault();

    let newErrors = { username: '', password: '' };

    if (!formData.username) {
      newErrors.username = 'Ingrese su usuario';
    }
    if (!formData.password) {
      newErrors.password = 'Ingrese su contraseña';
    }

    setErrors(newErrors);

    if (!newErrors.username && !newErrors.password) {
      navigate('/');
    }
  };

  return (
    <form className="flex w-full flex-col gap-10">
      <span className="flex flex-col gap-5">
        <span className="flex flex-col items-start">
          <label htmlFor="username">Usuario</label>
          <Input
            name="username"
            placeholder="usuario"
            type="text"
            value={formData.username}
            onChange={handleChange}
          />
          {errors.username && (
            <span className="text-sm text-red-500">{errors.username}</span>
          )}
        </span>

        <span className="flex flex-col items-start">
          <label htmlFor="password">Contraseña</label>
          <Input
            name="password"
            placeholder="Contraseña"
            type="password"
            value={formData.password}
            onChange={handleChange}
          />
          {errors.password && (
            <span className="text-sm text-red-500">{errors.password}</span>
          )}
        </span>
      </span>
      <SendFormButton text="Ingresar" onClick={handlerForm} />
    </form>
  );
};
