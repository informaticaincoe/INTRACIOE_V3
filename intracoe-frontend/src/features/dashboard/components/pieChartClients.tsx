import { useCallback, useState } from 'react';
import { Cell, Pie, PieChart, ResponsiveContainer } from 'recharts';
import { useTopClientes } from '../hooks/useTotalesPorTipo';

const COLORS = ['#232c6e', '#FCA94E', '#4DA1A9', '#FE6D73', '#8367C7'];

export const PieChartClients = () => {
  const [activeIndex, setActiveIndex] = useState(0);
  const onPieEnter = useCallback((_: any, index: number) => {
    setActiveIndex(index);
  }, []);

  const { clientes, loadingclientes } = useTopClientes();
  const pieData = clientes.map((c) => ({
    name: c.dtereceptor__nombre,
    value: c.total_ventas,
  }));

  const total = pieData.reduce((s, e) => s + e.value, 0);
  const top = pieData[0] || { name: '', value: 0 };

  // Truncado central con tooltip
  const MAX_NAME = 20;
  const displayName =
    top.name.length > MAX_NAME
      ? `${top.name.slice(0, MAX_NAME)}…`
      : top.name;

  return (
    <div style={{ width: '100%', maxWidth: 500, margin: '0 auto' }}>
      <ResponsiveContainer width="100%" height={350}>
        {loadingclientes ? (
          <p>Cargando...</p>
        ) : (
          <PieChart>
            <Pie
              data={pieData}
              dataKey="value"
              nameKey="name"
              cx="50%"
              cy="50%"
              innerRadius={80}
              outerRadius={120}
              activeIndex={activeIndex}
              onMouseEnter={onPieEnter}
            >
              {pieData.map((_, idx) => (
                <Cell
                  key={`cell-${idx}`}
                  fill={COLORS[idx % COLORS.length]}
                />
              ))}
            </Pie>

            {/* Nombre en el centro */}
            <text
              x="50%"
              y="45%"
              textAnchor="middle"
              dominantBaseline="middle"
              fontSize={16}
              fontWeight="600"
              style={{ pointerEvents: 'all', cursor: 'default' }}
            >
              <title>{top.name}</title>
              {displayName}
            </text>
            <text
              x="50%"
              y="55%"
              textAnchor="middle"
              dominantBaseline="middle"
              fontSize={20}
              fontWeight="700"
            >
              ${top.value.toLocaleString()}
            </text>
          </PieChart>
        )}
      </ResponsiveContainer>

      {/* Leyenda responsiva con Grid */}
      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          gap: 16,
          marginTop: 24,
        }}
      >
        {pieData.map((entry, idx) => {
          const percent = ((entry.value / total) * 100).toFixed(0);
          return (
            <div
              key={entry.name}
              style={{
                display: 'flex',
                flexDirection: 'column',
              }}
            >
              {/* Fila 1: punto y nombre */}
              <div
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  marginBottom: 4,
                }}
              >
                <span
                  style={{
                    width: 10,
                    height: 10,
                    borderRadius: '50%',
                    backgroundColor: COLORS[idx % COLORS.length],
                    display: 'inline-block',
                    marginRight: 8,
                  }}
                />
                <span
                  style={{
                    whiteSpace: 'nowrap',
                    overflow: 'hidden',
                    textOverflow: 'ellipsis',
                  }}
                  title={entry.name}
                >
                  {entry.name}
                </span>
              </div>

              {/* Fila 2: monto y porcentaje */}
              <div
                style={{
                  display: 'flex',
                  alignItems: 'baseline',
                  marginLeft: 18, // para alinear bajo el texto
                }}
              >
                <span style={{ marginRight: 8 }}>
                  ${entry.value.toLocaleString()}
                </span>
                <span style={{ color: '#666' }}>{percent}%</span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
