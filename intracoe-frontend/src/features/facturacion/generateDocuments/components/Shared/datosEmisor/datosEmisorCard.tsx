interface DatosEmisorCardInterface {
  nit: string;
  nombre: string;
  telefono: string;
  email: string;
  direccion_comercial: string;
}

export const DatosEmisorCard: React.FC<DatosEmisorCardInterface> = ({
  nit,
  nombre,
  telefono,
  email,
  direccion_comercial,
}) => {
  return (
    <>
      <div className="grid grid-cols-[auto_1fr] items-start justify-start gap-x-10 gap-y-4 font-medium">
        <span className="text-start text-black opacity-50">NIT:</span>
        <span className="text-start">{nit}</span>
        <span className="text-start text-black opacity-50">Nombre:</span>
        <span className="text-start">{nombre}</span>
        <span className="text-start text-black opacity-50">Teléfono:</span>
        <span className="text-start">{telefono}</span>
        <span className="text-start text-black opacity-50">Correo:</span>
        <span className="text-start">{email}</span>
        <span className="text-start text-black opacity-50">
          Dirección comercial:
        </span>
        <span className="text-start">{direccion_comercial}</span>
      </div>
    </>
  );
};
