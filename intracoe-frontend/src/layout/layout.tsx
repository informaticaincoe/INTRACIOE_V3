import { Outlet } from 'react-router';
import { Footer } from '../shared/footer/footer';
import { HeaderMenu } from '../shared/header/headerMenu';
import { SideMenu } from '../layout/components/sideMenu';

export const Layout = () => {
  return (
    <div className="flex h-screen flex-col justify-between">
      <HeaderMenu />
      <div className="flex h-full w-full">
        <SideMenu />
        <div className="flex w-full flex-col justify-between">
          <article className="">
            <Outlet />
          </article>

          <Footer />
        </div>
      </div>
    </div>
  );
};
