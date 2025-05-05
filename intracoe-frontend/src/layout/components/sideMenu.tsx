import { MdDashboard } from 'react-icons/md';
import { BsBuildingFill } from 'react-icons/bs';
import { FaCalculator } from 'react-icons/fa';
import { HiCurrencyDollar } from 'react-icons/hi2';
import { RiFilePaperFill } from 'react-icons/ri';
import { FaTruckRampBox } from 'react-icons/fa6';
import type { MenuProps } from 'antd';
import { Menu } from 'antd';
import { useNavigate } from 'react-router';
import { useState } from 'react';
import { CardModal } from '../../features/POST/components/cardModal';

type MenuItem = Required<MenuProps>['items'][number];

const items: MenuItem[] = [
  {
    key: 'dashboard',
    icon: <MdDashboard size={20} />,
    label: (
      <p className="m-0 text-start text-[0.9em] leading-tight break-words whitespace-normal">
        Dashboard
      </p>
    ),
  },
  {
    key: 'ventas',
    icon: <HiCurrencyDollar size={20} />,
    label: (
      <p className="m-0 text-start text-[0.9em] leading-tight break-words whitespace-normal">
        Ventas
      </p>
    ),
    children: [
      {
        key: 'receptores',
        label: (
          <p className="m-0 text-start text-[0.9em] leading-tight break-words whitespace-normal">
            clientes
          </p>
        ),
      },
      {
        key: 'proveedor',
        label: (
          <p className="m-0 text-start text-[0.9em] leading-tight break-words whitespace-normal">
            Proveedores
          </p>
        ),
      },
      {
        key: 'compras',
        label: (
          <p className="m-0 text-start text-[0.9em] leading-tight break-words whitespace-normal">
            Compras
          </p>
        ),
      },
    ],
  },
  {
    key: 'conta',
    icon: <FaCalculator size={20} />,
    label: (
      <p className="m-0 text-start text-[0.9em] leading-tight break-words whitespace-normal">
        Contabilidad
      </p>
    ),
    children: [
      {
        key: 'anexo',
        label: (
          <p className="m-0 text-start text-[0.9em] leading-tight break-words whitespace-normal">
            Anexos
          </p>
        ),
      },
      {
        key: 'reportes',
        label: (
          <p className="m-0 text-start text-[0.9em] leading-tight break-words whitespace-normal">
            Reportes
          </p>
        ),
      },
      {
        key: 'catalogo',
        label: (
          <p className="m-0 text-start text-[0.9em] leading-tight break-words whitespace-normal">
            Catalogo
          </p>
        ),
      },
    ],
  },
  {
    key: 'fact',
    icon: <RiFilePaperFill size={20} />,
    label: (
      <p className="m-0 text-start text-[0.9em] leading-tight break-words whitespace-normal">
        Facturación
      </p>
    ),

    children: [
      {
        key: 'documentos',
        label: (
          <p className="m-0 text-start text-[0.9em] leading-tight break-words whitespace-normal">
            Generar facturas
          </p>
        ),
      },
      {
        key: 'correcciones',
        label: (
          <p className="m-0 text-start text-[0.9em] leading-tight break-words whitespace-normal">
            Generar corecciones
          </p>
        ),
      },
      {
        key: 'listado-facturas',
        label: (
          <p className="m-0 text-start text-[0.9em] leading-tight break-words whitespace-normal">
            Listado Facturas
          </p>
        ),
      },
      {
        key: 'listado-contingencias',
        label: (
          <p className="m-0 text-start text-[0.9em] leading-tight break-words whitespace-normal">
            Listado contingencias
          </p>
        ),
      },
      {
        key: 'post',
        label: (
          <p className="m-0 text-start text-[0.9em] leading-tight break-words whitespace-normal">
            POST
          </p>
        ),
      },
    ],
  },
  {
    key: 'inventario',
    icon: <FaTruckRampBox size={20} />,
    label: (
      <p className="m-0 text-start text-[0.9em] leading-tight break-words whitespace-normal">
        Inventario
      </p>
    ),
    children: [
      {
        key: 'inventario',
        label: (
          <p className="m-0 text-start text-[0.9em] leading-tight break-words whitespace-normal">
            Movimientos de inventario
          </p>
        ),
      },
      {
        key: 'ajusteInventario',
        label: (
          <p className="m-0 text-start text-[0.9em] leading-tight break-words whitespace-normal">
            Ajuste de inventario
          </p>
        ),
      },
      {
        key: 'producto',
        label: (
          <p className="m-0 text-start text-[0.9em] leading-tight break-words whitespace-normal">
            Productos
          </p>
        ),
      },
      {
        key: 'servicios',
        label: (
          <p className="m-0 text-start text-[0.9em] leading-tight break-words whitespace-normal">
            Servicios{' '}
          </p>
        ),
      },
    ],
  },
  {
    key: 'empresa',
    icon: <BsBuildingFill size={20} />,
    label: (
      <p className="m-0 text-start text-[0.9em] leading-tight break-words whitespace-normal">
        Empresa
      </p>
    ),
    children: [
      {
        key: 'configuracion',
        label: (
          <p className="m-0 text-start text-[0.9em] leading-tight break-words whitespace-normal">
            Configurar empresa
          </p>
        ),
      },
      {
        key: 'server',
        label: (
          <p className="m-0 text-start text-[0.9em] leading-tight break-words whitespace-normal">
            Configurar servidor
          </p>
        ),
      },
    ],
  },
];

export const SideMenu = () => {
  const [visible, setVisible] = useState<boolean>(false);
  const navigate = useNavigate(); // Hook para navegar en React Router

  const onClick: MenuProps['onClick'] = (e) => {
    switch (e.key) {
      case 'dashboard':
        navigate('/dashboard');
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
      case 'inventario':
        navigate('/movimiento-inventario');
        break;
      case 'ajusteInventario':
        navigate('/ajuste-inventario');
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
        navigate('/proveedores');
        break;
      case 'compras':
        navigate('/compras');
        break;
      case 'post':
        setVisible(true)
        break;
      default:
        break;
    }
  };

  return (
    <div className="sticky flex h-full flex-col justify-between bg-white">
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
      <CardModal visible={visible} setVisible={setVisible} />
    </div>
  );
};
