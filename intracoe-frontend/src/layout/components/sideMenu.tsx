import { MdDashboard } from 'react-icons/md';
import { IoMdPerson } from 'react-icons/io';
import { HiCurrencyDollar } from 'react-icons/hi2';
import { RiFilePaperFill } from 'react-icons/ri';
import type { MenuProps } from 'antd';
import { Menu } from 'antd';
import { useNavigate } from 'react-router';

type MenuItem = Required<MenuProps>['items'][number];

const items: MenuItem[] = [
  {
    key: 'dashboard',
    icon: <MdDashboard size={24} />,
    label: <p className="text-start">Dashboard</p>,
  },
  {
    key: 'rrhh',
    icon: <IoMdPerson size={24} />,
    label: <p className="text-start">RRHH</p>,
  },
  {
    key: 'conta',
    icon: <HiCurrencyDollar size={24} />,
    label: <p className="text-start">Contabilidad</p>,
  },
  {
    key: 'fact',
    icon: <RiFilePaperFill size={24} />,
    label: <p className="text-start">Facturación</p>,

    children: [
      {
        key: 'fe',
        label: <p className="text-start">Facturación electronica</p>,
        children: [
          {
            key: 'act',
            label: <p className="text-start">Actividades economicas </p>,
          },
          {
            key: 'documentos',
            label: <p className="text-start">Generar documentos</p>,
          },
        ],
      },
      {
        key: 'empresa',
        label: <p className="text-start">Empresa</p>,
        children: [
          {
            key: 'producto',
            label: <p className="text-start">Producto</p>,
          },
          {
            key: 'servicios',
            label: <p className="text-start">Servicios</p>,
          },
          {
            key: 'configuracion',
            label: <p className="text-start">Configurar empresa</p>,
          },
        ],
      },
    ],
  },
];

export const SideMenu = () => {
  const navigate = useNavigate(); // Hook para navegar en React Router

  const onClick: MenuProps['onClick'] = (e) => {
    console.log('click ', e);

    switch (e.key) {
      case 'dashboard':
        navigate('/');
        break;
      case 'act':
        navigate('/actividades-economicas');
        break;
      case 'documentos':
        navigate('/generar-documentos');
        break;
      case 'producto':
        navigate('/productos');
        break;
      case 'servicios':
        navigate('/servicios');
        break;
      case 'configuracion':
        navigate('/empresa');
        break;
      default:
        break;
    }
  };

  return (
    <div className="h-full bg-white">
      <Menu
        onClick={onClick}
        style={{
          width: 300,
          opacity: '75%',
          fontFamily: 'Inter',
          position: 'sticky',
          top: 80,
        }}
        defaultSelectedKeys={['1']}
        defaultOpenKeys={['dashboard']}
        mode="inline"
        items={items}
      />
    </div>
  );
};
