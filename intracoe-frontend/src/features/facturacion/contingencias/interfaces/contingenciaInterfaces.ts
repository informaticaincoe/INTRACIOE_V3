export interface Contingencias {
  count: number;
  next: string;
  previous: string;
  results: ResltsContingencias[];
}

export interface ResltsContingencias {
  id: number;
  recibido_mh: boolean;
  sello_recepcion: string;
}

export interface FilterContingencia {
  recibido_mh: boolean | null;
  sello_recepcion: string | null;
  has_sello_recepcion: boolean | null;
  tipo_dte: any | null;
}
