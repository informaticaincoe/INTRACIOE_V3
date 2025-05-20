import { useEffect, useState } from "react";
import { useSearchParams } from "react-router";
import { Pagination } from "../../../../../../shared/interfaces/interfacesPagination";
import { Divider } from "antd";
import { TablaProductosPorProveedorSelector } from "./tablaProductosPorProveedorSelector";
import { ProductosProveedorInterface } from "../../../../../../shared/interfaces/interfaceFacturaJSON";
import { getProductosProveedores } from "../../../../../../shared/services/productos/productosServices";

interface ContenedorTablaProductosPorProveedoresProps {
  selectedProveedores: any;
  setSelectedProducts: any;
  selectedProducts: any
  setCantidadListProducts: any;
  setIdListProducts: any;
  setDescuentoItem: any;
}

export const ContenedorTablaProductosPorProveedores: React.FC<ContenedorTablaProductosPorProveedoresProps> = ({
  selectedProveedores,
  setSelectedProducts,
  selectedProducts,
  setCantidadListProducts,
  setIdListProducts,
  setDescuentoItem,
}) => {
  const [searchParams, setSearchParams] = useSearchParams();
  const [loading, setLoading] = useState(false);
  const [showModalAgregar, setShowModalAgregar] = useState(false)
  const [productosProveedorList, setProductosProveedorList] = useState<ProductosProveedorInterface>({
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
    if (!selectedProveedores?.id) return;
    fetchProductosPorProveedor();
  }, [selectedProveedores]);


  useEffect(() => {
    setPagination((prev) => ({ ...prev, current_page: 1 }));
    fetchProductosPorProveedor(1, pagination.page_size); //enviar el numero de pagina actual 1 por defecto, enviar la cantidad de elementos en pagina
  }, []);

  const updateListProductosProveedores = () => {
    fetchProductosPorProveedor(pagination.current_page);
  };

  const onPageChange = (event: any) => {
    const page = event.page + 1;
    const limit = event.rows;
    fetchProductosPorProveedor(page, limit);
  };

  const fetchProductosPorProveedor = async (page = 1, limit = 5) => {
    try {
      setLoading(true);
      const response = await getProductosProveedores(selectedProveedores.id, { page, limit });
      console.log("RESPUSETA DESDE CONTENEDOR", response)
      if (response) {
        console.log("responsessssss", response)
        setProductosProveedorList(response);
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
              {/* <ModalSujetoExcluidos visible={showModalAgregar} setVisible={setShowModalAgregar} update={updateListProductosProveedores}/> */}
            </div>
          }

          {/* <TablaProveedoresSelectorHeader
                        codigo={codigoFiltro}
                        onSearch={handleSearch}
                        setShowModalAgregar={setShowModalAgregar}
                        showModalAgregar={showModalAgregar}
                    /> */}
          <Divider />
          <TablaProductosPorProveedorSelector
            pagination={pagination}
            onPageChange={onPageChange}
            productoProveedoresList={productosProveedorList}
            // updateList={updateListProductosProveedores}
            setSelectedProducts={setSelectedProducts}
            selectedProducts={selectedProducts}
            setCantidadListProducts={setCantidadListProducts}
            setIdListProducts={setIdListProducts}
          />
        </>
      </div>
    </>
  );
};
