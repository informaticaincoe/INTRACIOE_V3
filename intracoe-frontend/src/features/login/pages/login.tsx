import { LoginForm } from '../components/loginForm';

export const Login = () => {
  return (
    <div>

      <section className='bg-white flex flex-col justify-center items-center'>
        <h1 className='text-5xl font-bold'><span className='text-primary-blue'>Intra</span><span className='text-primary-yellow'>coe</span></h1>
       <span className='py-5'>
         <h2 className='font-medium text-2xl '>Inicio de sesión</h2>
         <h3 className='text-light-text'>¡Bienvenido/a!</h3>
       </span>
        <LoginForm />
      </section>
    </div>
  );
};
