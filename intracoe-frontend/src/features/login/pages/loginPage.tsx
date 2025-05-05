import { useEffect } from 'react';
import { Footer } from '../../../shared/footer/footer';
import { HeaderMenu } from '../../../shared/header/headerMenu';
import { LoginForm } from '../components/loginForm';
import { removeCookie } from 'typescript-cookie';

export const Login = () => {
  useEffect(() => {
    removeCookie('authToken');
    removeCookie('csrftoken');
    removeCookie('sessionid');
  }, []);

  return (
    <div className="flex h-screen flex-col justify-between gap-10">
      <HeaderMenu />
      <div className="flex flex-col items-center">
        <section className="flex w-md flex-col items-center justify-center rounded-md bg-white px-10 py-5">
          <div className="flex flex-col gap-2">
            <h1 className="text-4xl font-bold">
              <span className="text-primary-blue">Intra</span>
              <span className="text-primary-yellow">coe</span>
            </h1>
            <span className="py-2">
              <h2 className="text-md font-bold">Inicio de sesión</h2>
              <h3 className="text-light-text text-sm">¡Bienvenido/a!</h3>
            </span>
          </div>
          <LoginForm />
        </section>
      </div>
      <Footer />
    </div>
  );
};
