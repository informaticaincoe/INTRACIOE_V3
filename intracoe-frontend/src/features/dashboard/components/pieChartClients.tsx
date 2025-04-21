import { useCallback, useState } from 'react'
import { Cell, Pie, PieChart, ResponsiveContainer, Sector } from 'recharts'
import { useTopClientes } from '../hooks/useTotalesPorTipo';

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

    const splitName = (name: string) => {
        const words = name.split(' ');
        const mid = Math.ceil(words.length / 2);
        return [words.slice(0, mid).join(' '), words.slice(mid).join(' ')];
    };

    const [line1, line2] = splitName(payload.name);
    const lines = `Total compras: $${value}`.split(' ');

    return (
        <g>
            <text x={cx} y={cy - 6} textAnchor="middle" fill={fill} fontSize={14}>
                {line1}
            </text>
            <text x={cx} y={cy + 10} textAnchor="middle" fill={fill} fontSize={14}>
                {line2}
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
                fontSize={14}
            >
                <tspan
                    x={ex + (cos >= 0 ? 1 : -1) * 24}
                    dy={0}
                >
                    Total compras:
                </tspan>
                <tspan
                    x={ex + (cos >= 0 ? 1 : -1) * 25}
                    dy={16}
                    fontWeight="bold"
                >
                    ${value}
                </tspan>
            </text>
            <text
                x={ex + (cos >= 0 ? 1 : -1) * 25}
                y={ey-20}
                dy={lines.length * 16 + 4} // mueve hacia abajo según cantidad de líneas
                textAnchor={textAnchor}
                fill="#999"
                fontSize={12}
            >
                {`(${(percent * 100).toFixed(2)}%)`}
            </text>

        </g>
    );
};


export const PieChartClients = () => {
    const [activeIndex, setActiveIndex] = useState(0);
    const onPieEnter = useCallback((_: any, index: number) => {
        setActiveIndex(index);
    }, []);

    const { clientes, loadingclientes } = useTopClientes();

    // 🔁 Transformamos los datos de la API
    const pieData = clientes.map((cliente) => ({
        name: cliente.dtereceptor__nombre,
        value: cliente.total_ventas,
    }));

    return (
        <ResponsiveContainer width="100%" height={450}>
            {loadingclientes ? <p>Cargando...</p> : <PieChart>
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
            </PieChart>}
        </ResponsiveContainer>
    );
};