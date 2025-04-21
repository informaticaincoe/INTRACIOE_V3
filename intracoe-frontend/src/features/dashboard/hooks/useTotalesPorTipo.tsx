// hooks/useTotalesPorTipo.ts
import { useEffect, useState } from 'react';
import { getClientes, getTotalesPorTipoDTE, getTotalVentas } from '../services/dashboardServices';

interface TotalPorTipo {
  tipo_dte: number;
  tipo_dte__codigo: string;
  total: number;
}

export const useTotalesPorTipo = () => {
  const [datos, setDatos] = useState<TotalPorTipo[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const result = await getTotalesPorTipoDTE();
        setDatos(result);
      } catch (error) {
        console.error("Error al obtener totales por tipo DTE:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  return { datos, loading };
};

export const useTotalFacturasEmitidas = () => {
  const [total, setTotal] = useState<number>(0);
  const [loadingTotal, setLoadingTotal] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const result = await getTotalesPorTipoDTE();

        // Sumar todos los `total` de los items
        const totalSumado = result.reduce(
          (acc: number, curr: { total: number }) => acc + curr.total,
          0
        );

        setTotal(totalSumado);
      } catch (error) {
        console.error("Error al obtener totales por tipo DTE:", error);
      } finally {
        setLoadingTotal(false);
      }
    };

    fetchData();
  }, []);

  return { total, loadingTotal }; // datos ahora es el total sumado
};

export const useTotalVentas = () => {
  const [totalVentas, setTotalVentas] = useState<number>(0);
  const [loadingTotalVentas, setLoadingTotalVentas] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const result = await getTotalVentas();
        setTotalVentas(result);
      } catch (error) {
        console.error("Error al obtener totales por tipo DTE:", error);
      } finally {
        setLoadingTotalVentas(false);
      }
    };

    fetchData();
  }, []);

  return { totalVentas, loadingTotalVentas }; // datos ahora es el total sumado
};

interface ClienteData {
  dtereceptor: number;
  dtereceptor__nombre: string;
  total_ventas: number;
}

export const useTopClientes = () => {
  const [clientes, setClientes] = useState<ClienteData[]>([]);
  const [loadingclientes, setLoadingclientes] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const result = await getClientes();
        setClientes(result);
      } catch (error) {
        console.error("Error al obtener totales por tipo DTE:", error);
      } finally {
        setLoadingclientes(false);
      }
    };

    fetchData();
  }, []);

  return { clientes, loadingclientes }; // datos ahora es el total sumado
};
