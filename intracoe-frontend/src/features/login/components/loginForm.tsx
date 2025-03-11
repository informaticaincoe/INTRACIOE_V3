import { useState } from 'react';
import { Input } from '../../../shared/forms/input';

export const LoginForm = () => {
  const [formData, setFormData] = useState({
    username: '',
    password: '',
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  return (
    <form className='flex flex-col gap-10'>
      <span>
        <span className="flex flex-col items-start">
          <label htmlFor="username">Usuario</label>
          <Input
            name="username"
            placeholder="usuario"
            type="text"
            value={formData.username}
            onChange={handleChange}
          />
        </span>
        <span className="flex flex-col items-start">
          <label htmlFor="password">Contraseña</label>
          <Input
            name="password"
            placeholder="Contraseña"
            type="text"
            value={formData.username}
            onChange={handleChange}
          />
        </span>
      </span>
      <button type="button" className='bg-primary-yellow text-white w-full py-3'>Ingresar</button>
    </form>
  );
};
