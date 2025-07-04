import { useEffect, useState } from "react";
import { useSearchParams } from "react-router";
import { ProveedorInterface } from "../../../../../ventas/proveedores/interfaces/proveedoresInterfaces";
import { Pagination } from "../../../../../../shared/interfaces/interfacesPagination";
import { getAllProveedores } from "../../../../../ventas/proveedores/services/proveedoresServices";
import { Title } from "../../../../../../shared/text/title";
import { WhiteSectionsPage } from "../../../../../../shared/containers/whiteSectionsPage";
import { TablaProveedoresHeader } from "../../../../../ventas/proveedores/componentes/tablaProveedoresHeader";
import { Divider } from "antd";
import { TablaProveedoresSelectorSelector } from "./tablaProveedoresSelector";
import { TablaProveedoresSelectorHeader } from "./tablaProveedoresSelectorHeader";
import { ModalSujetoExcluidos } from "./modalSujetoExcluido";

interface ContenedorTablaProveedores {
    selectedProveedores: any;
    setSelectedProveedores: any;
}

export const ContenedorTablaProveedores: React.FC<ContenedorTablaProveedores> = ({
    selectedProveedores,
    setSelectedProveedores
}) => {
    const [searchParams, setSearchParams] = useSearchParams();
    const [loading, setLoading] = useState(false);
    const [showModalAgregar, setShowModalAgregar] = useState(false)
    const [proveedorList, setProveedorList] = useState<ProveedorInterface>({
        count: 1,
        current_page: 1,
        page_size: 5,
        has_next: true,
        has_previous: false,
        results: [],
    });
    const [codigoFiltro, setCodigoFiltro] = useState<string>('');
    const [pagination, setPagination] = useState<Pagination>({
        count: 1,
        current_page: 1,
        page_size: 5,
        has_next: true,
        has_previous: false,
    });

    useEffect(() => {
        fetchProveedores();
    }, []);

    useEffect(() => {
        setPagination((prev) => ({ ...prev, current_page: 1 }));
        fetchProveedores(1, pagination.page_size); //enviar el numero de pagina actual 1 por defecto, enviar la cantidad de elementos en pagina
    }, []);

    const updateListProveedores = () => {
        fetchProveedores(pagination.current_page);
    };

    const onPageChange = (event: any) => {
        const page = event.page + 1;
        const limit = event.rows;
        fetchProveedores(page, limit);
    };

    const fetchProveedores = async (page = 1, limit = 5) => {
        try {
            setLoading(true);
            const response = await getAllProveedores({ page, limit });
            if (response) {
                setProveedorList(response);
                setPagination({
                    count: response.count || 0,
                    current_page: response.current_page || 1,
                    page_size: response.page_size || limit,
                    has_next: response.has_next,
                    has_previous: response.has_previous,
                });

                const params: Record<string, string> = {
                    page: String(response.current_page),
                    page_size: String(response.page_size),
                    // date_from: initialDateFrom,        // <-- futuro: filtro fecha
                    // date_to:   initialDateTo,
                };
                setSearchParams(params, { replace: true });
            } else {
                setPagination({
                    count: 1,
                    current_page: 1,
                    page_size: 5,
                    has_next: true,
                    has_previous: false,
                });
            }
        } catch (error) {
            console.log(error);
        }
    };

    const handleSearch = (nuevoCodigo: string) => {
        setCodigoFiltro(nuevoCodigo.trim());
    };

    return (
        <>
            <div className="border border-border-color rounded-md p-10">
                <>
                    {
                        showModalAgregar &&
                        <div className="absolute z-20">
                            <ModalSujetoExcluidos visible={showModalAgregar} setVisible={setShowModalAgregar} update={updateListProveedores}/>
                        </div>
                    }

                    <TablaProveedoresSelectorHeader
                        codigo={codigoFiltro}
                        onSearch={handleSearch}
                        setShowModalAgregar={setShowModalAgregar}
                        showModalAgregar={showModalAgregar}
                    />
                    <Divider />
                    <TablaProveedoresSelectorSelector
                        pagination={pagination}
                        onPageChange={onPageChange}
                        proveedoresList={proveedorList.results}
                        updateList={updateListProveedores}
                        selectedProveedores={selectedProveedores}
                        setSelectedProveedores={setSelectedProveedores}
                    />
                </>
            </div>
        </>
    );
};
