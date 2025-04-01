interface CondicionOperacionProps {
  condicion: number;
}

export const CondicionOperacion: React.FC<CondicionOperacionProps> = ({
  condicion,
}) => {
  return (
    <div className="border-border-color rounded-md border-2 px-4 py-3 text-start">
      <p>
        <span className="font-bold">Condicion de operación: </span>
        {condicion}
      </p>
    </div>
  );
};
