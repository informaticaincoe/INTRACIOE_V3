interface PagoEnLetrasInterfaceProps {
  cantidadAPagar: string;
}

export const PagoEnLetras: React.FC<PagoEnLetrasInterfaceProps> = ({
  cantidadAPagar,
}) => {
  return (
    <div className="border-border-color rounded-md border-2 px-4 py-3 text-start">
      <p>
        <span className="font-bold">Son: </span>
        {cantidadAPagar}
      </p>
    </div>
  );
};
