import { Route, BrowserRouter, Routes } from 'react-router';
import './App.css';
import './index.css';
import { lazily } from 'react-lazily';
import { Skeleton } from 'antd';

import 'primereact/resources/themes/lara-light-blue/theme.css';

import { Login } from './features/login/pages/loginPage';
import { Layout } from './layout/layout';
import { Dashboard } from './features/dashboard/pages/dashboard';
const { ActivitiesPage } = lazily(
  () => import('./features/facturacion/activities/pages/activitiesPage')
);

const { GenerateDocuments } = lazily(
  () =>
    import('./features/facturacion/generateDocuments/pages/GenerateDocuments')
);

const { UploadExcelPage } = lazily(
  () => import('./features/facturacion/activities/pages/uploadExcelPage')
);
const { ConfigBussiness } = lazily(
  () => import('./features/bussiness/configBussiness/pages/ConfigBussiness')
);
const { FacturaVisualizacionPage } = lazily(
  () =>
    import(
      './features/facturacion/PreFactura/pages/FE/facturaVisualizacionPage'
    )
);
const { ListadoFacturas } = lazily(
  () => import('./features/facturacion/Listadofacturas/pages/listadoFacturas')
);
const { GenerarDocumentosAjuste } = lazily(
  () =>
    import(
      './features/facturacion/generateDocuments/pages/generarDocumentosAjuste'
    )
);
const { ProductsPage } = lazily(
  () => import('./features/inventario/products/pages/productsPage')
);
const { NuevoProductoPage } = lazily(
  () => import('./features/inventario/products/pages/nuevoProductoPage')
);
const { ServicioPage } = lazily(
  () => import('./features/inventario/servicios/pages/servicioPage')
);
const { ReceptoresPage } = lazily(
  () => import('./features/ventas/receptores/pages/receptoresPage')
);
const { NuevoServiciopage } = lazily(
  () => import('./features/inventario/servicios/pages/nuevoServiciopage')
);
const { NuevoReceptorPage } = lazily(
  () => import('./features/ventas/receptores/pages/nuevoReceptorsPage')
);
const { CatalogosPage } = lazily(
  () => import('./features/contabilidad/catalogos/pages/catalogosPage')
);

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route index path="/login" element={<Login />} />
        <Route element={<Layout />}>
          <Route path="/" element={<Dashboard />} />
          <Route path="/actividades-economicas" element={<ActivitiesPage />} />
          <Route path="/generar-documentos" element={<GenerateDocuments />} />
          <Route
            path="/generar-documentos-ajuste"
            element={<GenerarDocumentosAjuste />}
          />
          <Route path="/factura/:id" element={<FacturaVisualizacionPage />} />
          <Route path="/productos" element={<ProductsPage />} />
          <Route path="/productos/nuevo" element={<NuevoProductoPage />} />
          <Route path="/producto/:id" element={<NuevoProductoPage />} />
          <Route path="/listado-facturas" element={<ListadoFacturas />} />
          <Route path="/servicios" element={<ServicioPage />} />
          <Route path="/servicio/nuevo" element={<NuevoServiciopage />} />
          <Route path="/servicio/:id" element={<NuevoServiciopage />} />
          <Route path="/empresa" element={<ConfigBussiness />} />
          <Route path="/receptores" element={<ReceptoresPage />} />
          <Route path="/catalogos" element={<CatalogosPage />} />
          <Route path="/receptor/nuevo" element={<NuevoReceptorPage />} />
          <Route path="/receptor/:id" element={<NuevoReceptorPage />} />
          <Route path="/uploadExcel" element={<UploadExcelPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
