import { Title } from "../../../shared/text/title";
import { WhiteCard } from "../components/whiteCard";
import totalVentasIcon from "../../../assets/total-ventas.svg"

export const Dashboard = () => {
  let total_ventas = 89935
  let total_facturas = 1750
  let producto_mas_vendido = "Leche ira 26"

  return (
    <>
      <Title text="Dashboard" />
      <div className="flex justify-between gap-10 px-10 my-10">
        <WhiteCard>
          <div className="flex justify-between">
            <span className="text-start flex flex-col gap-2">
              <h1 className="font-medium">Total ventas</h1>
              <p className="text-3xl font-bold">${total_ventas}</p>
            </span>
            <span className="bg-secondary-yellow-light size-10 flex rounded-md items-center justify-center ">
              <img src={totalVentasIcon} className="size"/>
            </span>
          </div>
        </WhiteCard>
        <WhiteCard>
          <span className="text-start flex flex-col gap-2">
            <h1 className="font-medium">Total facturas emitidas</h1>
            <p className="text-3xl font-bold">{total_facturas}</p>
          </span>
        </WhiteCard>
        <WhiteCard>
          <span className="text-start flex flex-col gap-2">
            <h1 className="font-medium">Producto con mas ventas</h1>
            <p className="text-3xl font-bold">{producto_mas_vendido}</p>
          </span>
        </WhiteCard>
      </div>
    </>
  );
};
