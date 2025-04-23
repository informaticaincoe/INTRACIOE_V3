import React from 'react'
import { WhiteCard } from '../whiteCard'
import { Statistic, StatisticProps } from 'antd'
import { CiFileOn } from 'react-icons/ci'
import { useTotalFacturasEmitidas } from '../../hooks/useTotalesPorTipo'
import CountUp from 'react-countup'

export const TotalFacturasEmitidasCard = () => {
    const { total, loadingTotal } = useTotalFacturasEmitidas();

    const formatterTotalFacturas: StatisticProps['formatter'] = (value) => (
        <CountUp
            end={value as number}
            separator=","
        >
            {({ countUpRef }) => (
                <span style={{ fontSize: '1.75rem', fontWeight: '600', height: '100%' }}>
                    <span ref={countUpRef} />
                </span>
            )}
        </CountUp>
    );

    return (
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
    )
}
