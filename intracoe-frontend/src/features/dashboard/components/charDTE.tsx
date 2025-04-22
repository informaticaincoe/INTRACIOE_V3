import { Chart } from 'react-google-charts';
import { useTotalesPorTipo } from '../hooks/useTotalesPorTipo';

export const ChartDTE = () => {
    const { datos, loading } = useTotalesPorTipo();

    const tipoDTE: { [key: string]: string } = {
        "01": "Factura",
        "03": "Credito fiscal",
        "05": "Nota de credito",
        "06": "Nota de debito",
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
        bars: 'vertical',
        colors: ['#232C6E'],
    };

    return (
        <div style={{ height: '400px' }}>
            {loading ?
                <p>Cargando gráfico...</p>
                :
                <Chart
                    chartType="Bar"
                    width="100%"
                    height="100%"
                    data={chartData}
                    options={options}
                />
            }
        </div>
    );
};
