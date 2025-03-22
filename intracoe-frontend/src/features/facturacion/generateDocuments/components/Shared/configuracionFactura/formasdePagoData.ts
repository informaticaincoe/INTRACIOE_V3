// Interfaz para representar un medio de pago
export interface PaymentMethodInteface {
  codigo: string;
  descripcion: string;
}

// Lista de medios de pago según los códigos y descripciones proporcionadas
export const paymentMethodsList: PaymentMethodInteface[] = [
  { codigo: '01', descripcion: 'Billetes y monedas' },
  { codigo: '02', descripcion: 'Tarjeta Débito' },
  { codigo: '03', descripcion: 'Tarjeta Crédito' },
  { codigo: '04', descripcion: 'Cheque' },
  { codigo: '05', descripcion: 'Transferencia-Depósito Bancario' },
  { codigo: '07', descripcion: 'Dinero electrónico' },
  { codigo: '08', descripcion: 'Dinero electrónico ' },
  { codigo: '09', descripcion: 'Monedero electrónico' },
  { codigo: '11', descripcion: 'Bitcoin' },
  { codigo: '12', descripcion: 'Otras Criptomonedas' },
  { codigo: '13', descripcion: 'Cuentas por pagar del receptor' },
  { codigo: '14', descripcion: 'Giro bancario' },
  { codigo: '99', descripcion: 'Otros' },
];
