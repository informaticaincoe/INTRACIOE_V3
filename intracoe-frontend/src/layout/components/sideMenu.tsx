import { MdDashboard } from 'react-icons/md';
import { BsBuildingFill } from 'react-icons/bs';
import { FaCalculator } from 'react-icons/fa';
import { HiCurrencyDollar } from 'react-icons/hi2';
import { RiFilePaperFill } from 'react-icons/ri';
import { FaTruckRampBox } from 'react-icons/fa6';
import type { MenuProps } from 'antd';
import { Menu } from 'antd';
import { useNavigate } from 'react-router';


type MenuItem = Required<MenuProps>['items'][number];

const items: MenuItem[] = [
  {
    key: 'dashboard',
    icon: <MdDashboard size={20} />,
    label: <p className="text-[0.9em] text-start whitespace-normal break-words leading-tight m-0">Dashboard</p>,
  },
  {
    key: 'ventas',
    icon: <HiCurrencyDollar size={20} />,
    label: <p className="text-[0.9em] text-start whitespace-normal break-words leading-tight m-0">Ventas</p>,
    children: [
      {
        key: 'receptores',
        label: <p className="text-[0.9em] text-start whitespace-normal break-words leading-tight m-0">clientes</p>,
      },
      {
        key: 'proveedor',
        label: <p className="text-[0.9em] text-start whitespace-normal break-words leading-tight m-0">Proveedores</p>,
      },
    ],
  },
  {
    key: 'conta',
    icon: <FaCalculator size={20} />,
    label: <p className="text-[0.9em] text-start whitespace-normal break-words leading-tight m-0">Contabilidad</p>,
    children: [
      {
        key: 'anexo',
        label: <p className="text-[0.9em] text-start whitespace-normal break-words leading-tight m-0">Anexos</p>,
      },
      {
        key: 'reportes',
        label: <p className="text-[0.9em] text-start whitespace-normal break-words leading-tight m-0">Reportes</p>,
      },
      {
        key: 'catalogo',
        label: <p className="text-[0.9em] text-start whitespace-normal break-words leading-tight m-0">Catalogo</p>,
      },
    ],
  },
  {
    key: 'fact',
    icon: <RiFilePaperFill size={20} />,
    label: <p className="text-[0.9em] text-start whitespace-normal break-words leading-tight m-0">Facturación</p>,

    children: [
      {
        key: 'documentos',
        label: <p className="text-[0.9em] text-start whitespace-normal break-words leading-tight m-0">Generar facturas</p>,
      },
      {
        key: 'correcciones',
        label: <p className="text-[0.9em] text-start whitespace-normal break-words leading-tight m-0">Generar corecciones</p>,
      },
      {
        key: 'listado-facturas',
        label: <p className="text-[0.9em] text-start whitespace-normal break-words leading-tight m-0">Listado Facturas</p>,
      },
      {
        key: 'listado-contingencias',
        label: <p className="text-[0.9em] text-start whitespace-normal break-words leading-tight m-0">Listado contingencias</p>,
      },
    ],
  },
  {
    key: 'inventario',
    icon: <FaTruckRampBox size={20} />,
    label: <p className="text-[0.9em] text-start whitespace-normal break-words leading-tight m-0">Inventario</p>,
    children: [
      {
        key: 'producto',
        label: <p className="text-[0.9em] text-start whitespace-normal break-words leading-tight m-0">Productos</p>,
      },
      {
        key: 'servicios',
        label: <p className="text-[0.9em] text-start whitespace-normal break-words leading-tight m-0">Servicios </p>,
      },
    ],
  },
  {
    key: 'empresa',
    icon: <BsBuildingFill size={20} />,
    label: <p className="text-[0.9em] text-start whitespace-normal break-words leading-tight m-0">Empresa</p>,
    children: [
      {
        key: 'configuracion',
        label: <p className="text-[0.9em] text-start whitespace-normal break-words leading-tight m-0">Configurar empresa</p>,
      },
      {
        key: 'server',
        label: <p className="text-[0.9em] text-start whitespace-normal break-words leading-tight m-0">Configurar servidor</p>,
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
      case 'listado-contingencias':
        navigate('/contingencias');
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
          width: '15vw',
          opacity: '75%',
          fontFamily: 'Inter',
          position: 'sticky',
          top: 80,
          whiteSpace: 'normal',
          wordWrap: 'break-word',
        }}
        defaultSelectedKeys={['1']}
        defaultOpenKeys={['dashboard']}
        mode="inline"
        items={items}
      />
    </div>
  );
};
