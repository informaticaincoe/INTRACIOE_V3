import { Route, BrowserRouter, Routes } from 'react-router';
import './App.css';
import { Login } from './features/login/pages/loginPage';
import { Layout } from './layout/layout';
import { Dashboard } from './features/dashboard/pages/dashboard';
import { ActivitiesPage } from './features/facturacion/activities/pages/activitiesPage';
import { GenerateDocuments } from './features/facturacion/generateDocuments/pages/GenerateDocuments';
import { UploadExcelPage } from './features/facturacion/activities/pages/uploadExcelPage';
import { ConfigBussiness } from './features/bussiness/configBussiness/pages/ConfigBussiness';
import { FacturaVisualizacionPage } from './features/facturacion/PreFactura/pages/FE/facturaVisualizacionPage';
import { ListadoFacturas } from './features/facturacion/Listadofacturas/pages/listadoFacturas';
import { GenerarDocumentosAjuste } from './features/facturacion/generateDocuments/pages/generarDocumentosAjuste';
import { ProductsPage } from './features/inventario/products/pages/productsPage';
import { NuevoProductoPage } from './features/inventario/products/pages/nuevoProductoPage';
import { ServicioPage } from './features/inventario/servicios/pages/servicioPage';
import { ReceptoresPage } from './features/ventas/receptores/pages/receptoresPage';
import { NuevoServiciopage } from './features/inventario/servicios/pages/nuevoServiciopage';
import { NuevoReceptorPage } from './features/ventas/receptores/pages/nuevoReceptorsPage';
import { CatalogosPage } from './features/contabilidad/pages/catalogosPage';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route index path="/login" element={<Login />} />
        <Route element={<Layout />}>
          <Route path="/" element={<Dashboard />} />
          <Route path="/actividades-economicas" element={<ActivitiesPage />} />
          <Route path="/generar-documentos" element={<GenerateDocuments />} />
          <Route path="/generar-documentos-ajuste" element={<GenerarDocumentosAjuste />} />
          <Route path="/factura/:id" element={<FacturaVisualizacionPage />} />
          <Route path="/productos" element={<ProductsPage />} />
          <Route path="/productos/nuevo" element={<NuevoProductoPage />} />
          <Route path="/producto/:id" element={<NuevoProductoPage />} />
          <Route path="/listado-facturas" element={<ListadoFacturas />} />
          <Route path="/servicios" element={<ServicioPage />} />
          <Route path="/servicio/nuevo" element={<NuevoServiciopage />} />
          <Route path="/servicio/:id" element={<NuevoServiciopage />} />
          <Route path="/empresa" element={<ConfigBussiness />} />
          <Route path="/receptores" element={<ReceptoresPage />}/>
          <Route path="/catalogos" element={<CatalogosPage />}/>
          <Route path="/receptor/nuevo" element={<NuevoReceptorPage />} />
          <Route path="/receptor/:id" element={<NuevoReceptorPage />} />
          <Route path="/uploadExcel" element={<UploadExcelPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
