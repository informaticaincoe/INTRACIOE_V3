import { Footer } from '../../../shared/footer/footer';
import { HeaderMenu } from '../../../shared/header/headerMenu';
import { LoginForm } from '../components/loginForm';

export const Login = () => {
  return (
    <div className="flex h-screen flex-col justify-between">
      <HeaderMenu />
      <div className="flex flex-col items-center">
        <section className="flex w-md flex-col items-center justify-center rounded-md bg-white px-10 py-10">
          <h1 className="text-5xl font-bold">
            <span className="text-primary-blue">Intra</span>
            <span className="text-primary-yellow">coe</span>
          </h1>
          <span className="py-10">
            <h2 className="text-xl font-bold">Inicio de sesión</h2>
            <h3 className="text-light-text">¡Bienvenido/a!</h3>
          </span>
          <LoginForm />
        </section>
      </div>
      <Footer />
    </div>
  );
};
