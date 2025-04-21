import { Chart } from 'react-google-charts';
import { useTotalesPorTipo } from '../hooks/useTotalesPorTipo';

export const ChartDTE = () => {
    const { datos, loading } = useTotalesPorTipo();

    if (loading) return <p>Cargando gráfico...</p>;

    const tipoDTE: { [key: string]: string } = {
        "01": "Factura",
        "03": "CCF",
        "05": "CNC",
        "06": "CND",
    };

    const chartData = [
        ['Tipo DTE', 'Total'],
        ...datos.map((item) => [
            tipoDTE[item.tipo_dte__codigo] || `Tipo ${item.tipo_dte__codigo}`,
            item.total,
        ]),
    ];


    const options = {
        chart: {
            title: 'Total de facturas',
            subtitle: 'intracoe',
        },
        bars: 'vertical', // fuerza orientación vertical
        colors: ['#232C6E'], // aquí sí “colors”
    };

    return (
        <div style={{ height: '400px' }}>
            <Chart
                chartType="Bar"
                width="100%"
                height="100%"
                data={chartData}
                options={options}
            />
        </div>
    );
};
