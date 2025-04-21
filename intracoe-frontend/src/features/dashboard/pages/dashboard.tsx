import { Title } from '../../../shared/text/title';
import { WhiteCard } from '../components/whiteCard';
/*icons*/
import { BsGraphUpArrow } from 'react-icons/bs';
import { CiFileOn } from 'react-icons/ci';
import { PiTag } from 'react-icons/pi';
import { useTotalFacturasEmitidas, useTotalVentas } from '../hooks/useTotalesPorTipo';
import { ChartDTE } from '../components/charDTE';
import { PieChartClients } from '../components/pieChartClients';
import { Statistic, StatisticProps } from 'antd';
import CountUp from 'react-countup';
import { TopProductosCarousel } from '../components/topProductosCarrusel';

const formatter: StatisticProps['formatter'] = (value) => (
  <CountUp
    end={value as number}
    decimals={2}
    decimal="."
    separator=","
  >
    {({ countUpRef }) => (
      <span style={{ fontSize: '1.75rem', fontWeight: '600' }}>
        $<span ref={countUpRef} />
      </span>
    )}
  </CountUp>
);

const formatterTotalFacturas: StatisticProps['formatter'] = (value) => (
  <CountUp
    end={value as number}
    separator=","
  >
    {({ countUpRef }) => (
      <span style={{ fontSize: '1.75rem', fontWeight: '600' }}>
        <span ref={countUpRef} />
      </span>
    )}
  </CountUp>
);


export const Dashboard = () => {
  let producto_mas_vendido = 'Leche ira 26';

  const { total, loadingTotal } = useTotalFacturasEmitidas();
  const { totalVentas, loadingTotalVentas } = useTotalVentas();

  return (
    <>
      <Title text="Dashboard" />
      <div className="my-10 grid grid-cols-3 justify-between gap-10 px-10 flex-1">
        <WhiteCard>
          <div className="flex justify-between flex-1">
            <span className="flex flex-col gap-2 text-start">
              <h1 className="font opacity-70">Total ventas</h1>
              {loadingTotalVentas ? <p>Cargando...</p> : <Statistic value={totalVentas} formatter={formatter} />}
            </span>
            <span className="bg-secondary-yellow-light flex size-10 items-center justify-center rounded-md">
              <BsGraphUpArrow size={24} color={'#FCC587'} />
            </span>
          </div>
        </WhiteCard>
        <WhiteCard>
          <div className="flex justify-between flex-1">
            <span className="flex flex-col gap-2 text-start">
              <h1 className="font opacity-70">Total facturas emitidas</h1>
              {loadingTotal ? <p>Cargando...</p> : <Statistic value={total} formatter={formatterTotalFacturas} />}
            </span>
            <span className="bg-secondary-yellow-light flex size-10 items-center justify-center rounded-md">
              <CiFileOn size={24} color={'#FCC587'} />
            </span>
          </div>
        </WhiteCard>
        <WhiteCard>
          <div className="flex justify-between">
            <span className="flex flex-col gap-2 text-start items w-5/6">
              <h1 className="font opacity-70">Producto con mas ventas</h1>
              <TopProductosCarousel />
            </span>
            <span className="bg-secondary-yellow-light flex size-10 items-center justify-center rounded-md">
              <PiTag size={24} color={'#FCC587'} />
            </span>
          </div>
        </WhiteCard>
      </div>

      <div className="grid w-full grid-cols-3 justify-between gap-10 px-10">
        <div className="col-span-2 flex w-full justify-between gap-10">
          <WhiteCard>
            <>
              <h1 className="text-xl font-semibold">Tipo de facturas</h1>
              <div>
                <ChartDTE />
              </div>
            </>
          </WhiteCard>
        </div>
        <div className="col-start-3 flex w-full justify-between">
          <WhiteCard>
            <>
              <h1 className="text-xl font-semibold">Top 3 clientes</h1>
              <PieChartClients />
            </>
          </WhiteCard>
        </div>
      </div>
    </>
  );
};
