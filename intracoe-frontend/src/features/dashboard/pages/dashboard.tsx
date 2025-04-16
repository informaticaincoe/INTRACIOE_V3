import { Title } from '../../../shared/text/title';
import { WhiteCard } from '../components/whiteCard';
import totalVentasIcon from '../../../assets/ventas-totales-icono.svg';
/*icons*/
import { BsGraphUpArrow } from 'react-icons/bs';
import { CiFileOn } from 'react-icons/ci';
import { PiTag } from 'react-icons/pi';
import { data, TopClientes } from './dataTest';
//

import { Chart } from 'react-google-charts';
import { PieChart, Pie, Sector, ResponsiveContainer, Cell } from 'recharts';
import { useCallback, useState } from 'react';

const RADIAN = Math.PI / 180;
const COLORS = ['#2E5077', '#4DA1A9', '#D7E8BA']; // ← define aquí tantos colores como quieras

const renderActiveShape = (props: any) => {
  const {
    cx,
    cy,
    midAngle,
    innerRadius,
    outerRadius,
    startAngle,
    endAngle,
    fill,
    payload,
    percent,
    value,
  } = props;
  const sin = Math.sin(-RADIAN * midAngle);
  const cos = Math.cos(-RADIAN * midAngle);
  const sx = cx + (outerRadius + 10) * cos;
  const sy = cy + (outerRadius + 10) * sin;
  const mx = cx + (outerRadius + 30) * cos;
  const my = cy + (outerRadius + 30) * sin;
  const ex = mx + (cos >= 0 ? 1 : -1) * 22;
  const ey = my;
  const textAnchor = cos >= 0 ? 'start' : 'end';

  return (
    <g>
      <text x={cx} y={cy} dy={8} textAnchor="middle" fill={fill}>
        {payload.name}
      </text>
      <Sector
        cx={cx}
        cy={cy}
        innerRadius={innerRadius}
        outerRadius={outerRadius}
        startAngle={startAngle}
        endAngle={endAngle}
        fill={fill}
      />
      <Sector
        cx={cx}
        cy={cy}
        startAngle={startAngle}
        endAngle={endAngle}
        innerRadius={outerRadius + 6}
        outerRadius={outerRadius + 10}
        fill={fill}
      />
      <path
        d={`M${sx},${sy}L${mx},${my}L${ex},${ey}`}
        stroke={fill}
        fill="none"
      />
      <circle cx={ex} cy={ey} r={2} fill={fill} stroke="none" />
      <text
        x={ex + (cos >= 0 ? 1 : -1) * 12}
        y={ey}
        textAnchor={textAnchor}
        fill="#333"
      >{`Facturas ${value}`}</text>
      <text
        x={ex + (cos >= 0 ? 1 : -1) * 12}
        y={ey}
        dy={18}
        textAnchor={textAnchor}
        fill="#999"
      >{`(${(percent * 100).toFixed(2)}%)`}</text>
    </g>
  );
};

export const Dashboard = () => {
  let total_ventas = 89935;
  let total_facturas = 1750;
  let producto_mas_vendido = 'Leche ira 26';

  const options = {
    chart: {
      title: 'Total de facturas',
      subtitle: 'intracoe',
    },
    bars: 'vertical', // fuerza orientación vertical
    colors: ['#232C6E'], // aquí sí “colors”
  };

  const [activeIndex, setActiveIndex] = useState(0);
  const onPieEnter = useCallback((_: any, index: number) => {
    setActiveIndex(index);
  }, []);

  // Mapeo directo de tu TopClientes
  const pieData = TopClientes.map(([name, value]) => ({ name, value }));

  const optionsClients = {
    pieHole: 0.4,
    is3D: false,
    colors: ['#232C6E', '#FCA94E', '#7B9E89'],
  };

  return (
    <>
      <Title text="Dashboard" />
      <div className="my-10 flex justify-between gap-10 px-10">
        <WhiteCard>
          <div className="flex justify-between">
            <span className="flex flex-col gap-2 text-start">
              <h1 className="font opacity-70">Total ventas</h1>
              <p className="text-3xl font-semibold">${total_ventas}</p>
            </span>
            <span className="bg-secondary-yellow-light flex size-10 items-center justify-center rounded-md">
              <BsGraphUpArrow size={24} color={'#FCC587'} />
            </span>
          </div>
        </WhiteCard>
        <WhiteCard>
          <div className="flex justify-between">
            <span className="flex flex-col gap-2 text-start">
              <h1 className="font opacity-70">Total facturas emitidas</h1>
              <p className="text-3xl font-semibold">{total_facturas}</p>
            </span>
            <span className="bg-secondary-yellow-light flex size-10 items-center justify-center rounded-md">
              <CiFileOn size={24} color={'#FCC587'} />
            </span>
          </div>
        </WhiteCard>
        <WhiteCard>
          <div className="flex justify-between">
            <span className="flex flex-col gap-2 text-start">
              <h1 className="font opacity-70">Producto con mas ventas</h1>
              <p className="text-3xl font-semibold">{producto_mas_vendido}</p>
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
                <Chart
                  chartType="Bar" // Material Bar Chart
                  width="100%"
                  height="50vh"
                  data={data}
                  options={options}
                />
              </div>
            </>
          </WhiteCard>
        </div>
        <div className="col-start-3 flex w-full justify-between">
          <WhiteCard>
            <>
              <h1 className="text-xl font-semibold">Top 3 clientes</h1>
              <ResponsiveContainer width="100%" height={450}>
                <PieChart>
                  <Pie
                    data={pieData}
                    dataKey="value"
                    nameKey="name"
                    cx="50%"
                    cy="50%"
                    innerRadius={100}
                    outerRadius={140}
                    activeIndex={activeIndex}
                    activeShape={renderActiveShape}
                    onMouseEnter={onPieEnter}
                  >
                    {pieData.map((_, index) => (
                      <Cell
                        key={`cell-${index}`}
                        fill={COLORS[index % COLORS.length]}
                      />
                    ))}
                  </Pie>
                </PieChart>
              </ResponsiveContainer>
            </>
          </WhiteCard>
        </div>
      </div>
    </>
  );
};
