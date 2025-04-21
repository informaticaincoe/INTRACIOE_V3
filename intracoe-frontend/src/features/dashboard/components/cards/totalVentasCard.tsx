import React from 'react'
import { WhiteCard } from '../whiteCard'
import { BsGraphUpArrow } from 'react-icons/bs'
import { useTotalVentas } from '../../hooks/useTotalesPorTipo';
import { Statistic, StatisticProps } from 'antd';
import CountUp from 'react-countup';

export const TotalVentas = () => {
    const { totalVentas, loadingTotalVentas } = useTotalVentas();

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

    return (
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
    )
}
