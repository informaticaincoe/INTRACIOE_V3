import { Title } from '../../../shared/text/title';
import { WhiteCard } from '../components/whiteCard';
import { ChartDTE } from '../components/charDTE';
import { PieChartClients } from '../components/pieChartClients';
import { TotalVentas } from '../components/cards/totalVentasCard';
import { TotalFacturasEmitidasCard } from '../components/cards/totalFacturasEmitidasCard';
import { ProductosMasVendidosCard } from '../components/cards/productosMasVendidosCard';

export const Dashboard = () => {

  return (
    <>
      <Title text="Dashboard" />
      <div className="my-10 grid grid-cols-3 justify-between gap-10 px-10 flex-1">
        <TotalVentas />
        <TotalFacturasEmitidasCard />
        <ProductosMasVendidosCard />
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
