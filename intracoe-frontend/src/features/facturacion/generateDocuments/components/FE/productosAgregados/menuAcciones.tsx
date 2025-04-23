import { Button } from 'primereact/button';
import { TieredMenu } from 'primereact/tieredmenu';
import { useRef } from 'react';

import { SlOptions } from 'react-icons/sl';

// Define types for menu items
interface MenuItem {
  label: string;
  icon?: string;
  items?: MenuItem[];
  separator?: boolean;
}

export const MenuAcciones = () => {
  const menu = useRef<any>(null);

  const items: MenuItem[] = [
    {
      label: 'Eliminar',
    },
    {
      label: 'Agregar tributo',
    },
  ];

  return (
    <div className="flex items-center justify-center">
      <TieredMenu model={items} popup ref={menu} breakpoint="767px" />
      <Button
        icon={<SlOptions />}
        className="m-0 flex rounded-md p-0 px-2 pt-2 hover:cursor-pointer hover:bg-gray-100"
        unstyled
        onClick={(e) => menu.current.toggle(e)}
      />
    </div>
  );
};
