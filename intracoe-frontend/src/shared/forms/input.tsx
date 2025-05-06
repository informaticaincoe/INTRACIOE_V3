interface InputProps {
  name: string;
  placeholder?: string;
  type?: 'text' | 'number' | 'email' | 'password' | 'date' | 'file';
  value: string;
  onChange: (event: React.ChangeEvent<HTMLInputElement>) => void;
  className?: string;
  required?: boolean;
  icon?: any;
  disable?:boolean;
}

export const Input: React.FC<InputProps> = ({
  name,
  placeholder = '',
  type,
  value,
  onChange,
  className,
  disable = false
}) => {
  return (
    <input
      disabled={disable}
      type={type}
      name={name}
      placeholder={placeholder}
      value={value}
      onChange={onChange}
      className={`border-border-color focus:outline-border w-full rounded-sm border px-3 py-3 focus:outline-1 ${className} ${disable ? 'bg-gray-200 cursor-not-allowed' : 'bg-transparent'}`}
    />
  );
};
