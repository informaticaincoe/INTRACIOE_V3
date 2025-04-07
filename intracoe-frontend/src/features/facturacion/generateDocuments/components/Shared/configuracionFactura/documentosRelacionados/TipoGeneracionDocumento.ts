export const TipoGeneracionDocumento: TipoGeneracionDocumentoInterface[] = [
  {
    id: 1,
    codigo: '1',
    descripcion: 'Fisico',
  },
  {
    id: 2,
    codigo: '2',
    descripcion: 'Electronico',
  },
];

export interface TipoGeneracionDocumentoInterface {
  id: number;
  codigo: string;
  descripcion: string;
}
