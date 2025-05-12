import { Route, BrowserRouter, Routes, Navigate } from 'react-router';
import './App.css';
import './index.css';
import { lazily } from 'react-lazily';

import 'primereact/resources/themes/lara-light-blue/theme.css';

import { Login } from './features/login/pages/loginPage';
import { Layout } from './layout/layout';
import { MovimientoInventarioEdit } from './features/inventario/movimientoInventario/pages/movimientoInventarioEditNew';
import { ProveedoresPage } from './features/ventas/proveedores/pages/proveedoresPage';
import { ProveedoresNewEdit } from './features/ventas/proveedores/pages/proveedoresNewEdit';
import { ComprasPage } from './features/compras/compras/pages/comprasPage';
import { ComprasNewEdit } from './features/compras/compras/pages/comprasEditNew';
import { AjusteInventarioPage } from './features/inventario/ajusteInventario/pages/ajusteInventarioPage';
import { AjusteInventarioEditNew } from './features/inventario/ajusteInventario/pages/ajusteInventarioEditNew';
import { DevoluacionesVentaPage } from './features/ventas/devolucioneVentas/pages/devolucionesVentaPage';
import { DevolucionesCompraPage } from './features/compras/devolucionesCompras/pages/devolucionesCompraPage';

const { Dashboard } = lazily(
  () => import('./features/dashboard/pages/dashboard')
);

const { ContingenciasPage } = lazily(
  () => import('./features/facturacion/contingencias/pages/contingenciasPage')
);

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

const { MovimientoInventarioPage } = lazily(
  () =>
    import(
      './features/inventario/movimientoInventario/pages/movimientoInventarioPage'
    )
);

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to="/login" replace />} />
        <Route path="/login" element={<Login />} />
        <Route element={<Layout />}>
          <Route path="/dashboard" element={<Dashboard />} />
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

          <Route
            path="/movimiento-inventario"
            element={<MovimientoInventarioPage />}
          />
          <Route
            path="/movimiento-inventario/:id"
            element={<MovimientoInventarioEdit />}
          />
          <Route
            path="/movimiento-inventario/nuevo"
            element={<MovimientoInventarioEdit />}
          />
          <Route path="/ajuste-inventario" element={<AjusteInventarioPage />} />
          <Route
            path="/ajuste-inventario/nuevo"
            element={<AjusteInventarioEditNew />}
          />
          <Route
            path="/ajuste-inventario/:id"
            element={<AjusteInventarioEditNew />}
          />

          <Route path="/servicio/nuevo" element={<NuevoServiciopage />} />
          <Route path="/servicio/:id" element={<NuevoServiciopage />} />
          <Route path="/empresa" element={<ConfigBussiness />} />
          <Route path="/receptores" element={<ReceptoresPage />} />
          <Route path="/proveedores" element={<ProveedoresPage />} />
          <Route path="/proveedores/nuevo" element={<ProveedoresNewEdit />} />
          <Route path="/proveedor/:id" element={<ProveedoresNewEdit />} />

          <Route path="/compras" element={<ComprasPage />} />
          <Route path="/compras/nuevo" element={<ComprasNewEdit />} />
          <Route path="/compras/:id" element={<ComprasNewEdit />} />

          <Route
            path="/devoluciones-compra"
            element={<DevolucionesCompraPage />}
          />
          <Route
            path="/devoluciones-ventas"
            element={<DevoluacionesVentaPage />}
          />

          <Route path="/catalogos" element={<CatalogosPage />} />
          <Route path="/receptor/nuevo" element={<NuevoReceptorPage />} />
          <Route path="/receptor/:id" element={<NuevoReceptorPage />} />
          <Route path="/uploadExcel" element={<UploadExcelPage />} />
          <Route path="/contingencias" element={<ContingenciasPage />} />
        </Route>
        <Route path="*" element={<Navigate to="/dashboard" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
