export interface Empresa {
    nit: string;
    nrc: string;
    nombre_razon_social: string;
    nombre_comercial: string;
    direccion_comercial: string;
    telefono: string;
    email: string;
    codigo_establecimiento: string;
    codigo_punto_venta: string;
    nombre_establecimiento: string | null;
    tipoestablecimiento: string;
    municipio: string;
    ambiente: string;
    tipo_documento: string;
    actividades_economicas: string[]; // Array de IDs de actividades económicas
}