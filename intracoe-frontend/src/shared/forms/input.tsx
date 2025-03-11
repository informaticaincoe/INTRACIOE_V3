interface InputProps {
  name: string;
  placeholder?: string;
  type?: 'text' | 'number' | 'email' | 'password' | 'date' | 'file';
  value: string;
  onChange: (event: React.ChangeEvent<HTMLInputElement>) => void;
  className?: string;
}

export const Input: React.FC<InputProps> = ({
  name,
  placeholder = '',
  type,
  value,
  onChange,
  className,
}) => {
  return (
    <input
      type={type}
      name={name}
      placeholder={placeholder}
      value={value}
      onChange={onChange}
      className={`border-border focus:outline-border rounded-sm border px-3 py-2 focus:outline-1 ${className}`}
    />
  );
};
