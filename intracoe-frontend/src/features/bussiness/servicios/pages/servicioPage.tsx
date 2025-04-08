import React, { useEffect, useState } from 'react';
import { Title } from '../../../../shared/text/title';
import { WhiteSectionsPage } from '../../../../shared/containers/whiteSectionsPage';
import { Divider } from 'antd';
import { TablaServiciosHeader } from '../componenetes/tablaServiciosHeader';
import { TablaContainerServicios } from '../componenetes/tablaContainerServicios';
import { ProductoResponse } from '../../../../shared/interfaces/interfaces';
import { getAllProducts } from '../../../../shared/services/productos/productosServices';

export const ServicioPage = () => {
    const [servicios, setServicios] = useState<ProductoResponse[]>([]);
    const [codigoFiltro, setCodigoFiltro] = useState<string>('');

    // Cada vez que cambie el filtro, recargamos los servicios
    useEffect(() => {
        fetchServicios();
    }, [codigoFiltro]);

    const fetchServicios = async () => {
        try {
            // Pasamos tipo=2 (servicios) y, si hay código, también filter
            const response = await getAllProducts({
                tipo: 2,
                filter: codigoFiltro || undefined
            });
            setServicios(response);
        } catch (error) {
            console.error(error);
        }
    };

    // Handler que pasamos al header para que active la búsqueda
    const handleSearch = (nuevoCodigo: string) => {
        setCodigoFiltro(nuevoCodigo.trim());
    };

    return (
        <>
            <Title text="Servicios" />
            <WhiteSectionsPage>
                <div>
                    <TablaServiciosHeader codigo={codigoFiltro} onSearch={handleSearch} />
                    <Divider />
                    <TablaContainerServicios servicios={servicios} refreshProducts={fetchServicios} />
                </div>
            </WhiteSectionsPage>
        </>
    );
};