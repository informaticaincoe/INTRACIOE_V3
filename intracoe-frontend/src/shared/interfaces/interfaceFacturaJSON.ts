export interface FacturaJSON {
    emisorJSON: EmisorJSON
}

export interface EmisorJSON {
    nit: string,
    nrc: string,
    nombre: string,
    codActividad: string,
    descActividad: string,
    nombreComercial: string,
    tipo_establecimiento_codigo: string,
    departamento: string,
    municipio: string,
    complemento: string
    telefono: string,
    correo: string,
    codEstableMH: string,
    codEstable: string,
    codPuntoVentaMH: string,
    codPuntoVenta: string

}