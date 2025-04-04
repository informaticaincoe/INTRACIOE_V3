import { Route, BrowserRouter, Routes } from 'react-router';
import './App.css';
import { Login } from './features/login/pages/loginPage';
import { Layout } from './layout/layout';
import { Dashboard } from './features/dashboard/pages/dashboard';
import { ActivitiesPage } from './features/facturacion/activities/pages/activitiesPage';
import { GenerateDocuments } from './features/facturacion/generateDocuments/pages/GenerateDocuments';
import { ProductsPage } from './features/bussiness/products/pages/productsPage';
import { UploadExcelPage } from './features/facturacion/activities/pages/uploadExcelPage';
import { ConfigBussiness } from './features/bussiness/configBussiness/pages/ConfigBussiness';
import { FacturaVisualizacionPage } from './features/facturacion/PreFactura/pages/FE/facturaVisualizacionPage';
import { ListadoFacturas } from './features/facturacion/Listadofacturas/pages/listadoFacturas';
import { NuevoProductoPage } from './features/bussiness/products/pages/nuevoProductoPage';
import { ServicioPage } from './features/bussiness/servicios/pages/servicioPage';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route index path="/login" element={<Login />} />
        <Route element={<Layout />}>
          <Route path="/" element={<Dashboard />} />
          <Route path="/actividades-economicas" element={<ActivitiesPage />} />
          <Route path="/generar-documentos" element={<GenerateDocuments />} />
          <Route path="/factura/:id" element={<FacturaVisualizacionPage />} />
          <Route path="/productos" element={<ProductsPage />} />
          <Route path="/productos/nuevo" element={<NuevoProductoPage />} />
          <Route path="/listado-facturas" element={<ListadoFacturas />} />
          <Route path="/servicios" element={<ServicioPage />} />
          <Route path="/empresa" element={<ConfigBussiness />} />
          <Route path="/uploadExcel" element={<UploadExcelPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
