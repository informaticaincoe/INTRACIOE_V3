import { MdDashboard } from 'react-icons/md';
import { IoMdPerson } from 'react-icons/io';
import { BsBuildingFill } from 'react-icons/bs';
import { FaCalculator } from 'react-icons/fa';
import { HiCurrencyDollar } from 'react-icons/hi2';
import { RiFilePaperFill } from 'react-icons/ri';
import { FaTruckRampBox } from 'react-icons/fa6';
import type { MenuProps } from 'antd';
import { Menu } from 'antd';
import { useNavigate } from 'react-router';

import defaultPerfil from "../../assets/default-perfil.png"

type MenuItem = Required<MenuProps>['items'][number];

const items: MenuItem[] = [
  {
    key: 'dashboard',
    icon: <MdDashboard size={24} />,
    label: <p className="text-start">Dashboard</p>,
  },
  {
    key: 'ventas',
    icon: <HiCurrencyDollar size={24} />,
    label: <p className="text-start">Ventas</p>,
    children: [
      {
        key: 'receptores',
        label: <p className="text-start">clientes</p>,
      },
      {
        key: 'proveedor',
        label: <p className="text-start">Proveedores</p>,
      },
    ],
  },
  {
    key: 'conta',
    icon: <FaCalculator size={24} />,
    label: <p className="text-start">Contabilidad</p>,
    children: [
      {
        key: 'anexo',
        label: <p className="text-start">Anexos</p>,
      },
      {
        key: 'reportes',
        label: <p className="text-start">Reportes</p>,
      },
      {
        key: 'catalogo',
        label: <p className="text-start">Catalogo</p>,
      },
    ],
  },
  {
    key: 'fact',
    icon: <RiFilePaperFill size={24} />,
    label: <p className="text-start">Facturación</p>,

    children: [
      {
        key: 'documentos',
        label: <p className="text-start">Generar facturas</p>,
      },
      {
        key: 'correcciones',
        label: <p className="text-start">Generar corecciones</p>,
      },
      {
        key: 'listado-facturas',
        label: <p className="text-start">Listado Facturas</p>,
      },
    ],
  },
  {
    key: 'inventario',
    icon: <FaTruckRampBox size={24} />,
    label: <p className="text-start">Inventario</p>,
    children: [
      {
        key: 'producto',
        label: <p className="text-start">Productos</p>,
      },
      {
        key: 'servicios',
        label: <p className="text-start">Servicios </p>,
      },
    ],
  },
  {
    key: 'empresa',
    icon: <BsBuildingFill size={24} />,
    label: <p className="text-start">Empresa</p>,
    children: [
      {
        key: 'configuracion',
        label: <p className="text-start">Configurar empresa</p>,
      },
      {
        key: 'server',
        label: <p className="text-start">Configurar servidor</p>,
      },
    ],
  },
];

export const SideMenu = () => {
  const navigate = useNavigate(); // Hook para navegar en React Router

  const onClick: MenuProps['onClick'] = (e) => {
    switch (e.key) {
      case 'dashboard':
        navigate('/');
        break;
      case 'documentos':
        navigate('/generar-documentos');
        break;
      case 'correcciones':
        navigate('/generar-documentos-ajuste');
        break;
      case 'catalogo':
        navigate('/catalogos');
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
      case 'receptores':
        navigate('/receptores');
        break;
      case 'listado-facturas':
        navigate('/listado-facturas');
        break;
      case 'proveedor':
        navigate('/proveedor');
        break;
      default:
        break;
    }
  };

  return (
    <div className="h-full bg-white flex flex-col justify-between sticky ">
      <Menu
        onClick={onClick}
        style={{
          width: 250,
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
