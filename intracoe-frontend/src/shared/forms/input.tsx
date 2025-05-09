interface InputProps {
  name: string;
  placeholder?: string;
  type?: 'text' | 'number' | 'email' | 'password' | 'date' | 'file';
  value: string;
  onChange: (event: React.ChangeEvent<HTMLInputElement>) => void;
  className?: string;
  required?: boolean;
  icon?: any;
  disable?: boolean;
  minNum?: number;
  step?: string;
}

export const Input: React.FC<InputProps> = ({
  name,
  placeholder = '',
  type,
  value,
  onChange,
  className,
  disable = false,
  minNum = 0,
  step,
}) => {
  return (
    <input
      min={minNum}
      step={step}
      disabled={disable}
      type={type}
      name={name}
      placeholder={placeholder}
      value={value}
      onChange={onChange}
      className={`border-border-color focus:outline-border w-full rounded-sm border px-3 py-3 focus:outline-1 ${className} ${disable ? 'text-gray cursor-not-allowed bg-gray-100' : 'bg-transparent'}`}
    />
  );
};
