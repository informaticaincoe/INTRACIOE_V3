export interface ProveedorInterface {
    id: number;
    nombre: string;
    ruc_nit: string;
    contacto?: string | null;
    telefono?: string | null;
    email?: string | null;
    direccion?: string | null;
    condiciones_pago?: string | null;
}
