import { LoginForm } from '../components/loginForm';

export const Login = () => {
  return (
    <div className='flex flex-col items-center'>
        <section className="flex flex-col items-center justify-center bg-white py-10 px-10 w-md rounded-md">
          <h1 className="text-5xl font-bold">
            <span className="text-primary-blue">Intra</span>
            <span className="text-primary-yellow">coe</span>
          </h1>
          <span className="py-10">
            <h2 className="text-2xl font-medium">Inicio de sesión</h2>
            <h3 className="text-light-text">¡Bienvenido/a!</h3>
          </span>
          <LoginForm />
        </section>
    </div>
  );
};
