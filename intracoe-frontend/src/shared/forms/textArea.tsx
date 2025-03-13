interface TextAreaProps {
  name: string;
  placeholder?: string;
  value: string;
  onChange: (event: React.ChangeEvent<HTMLTextAreaElement>) => void;
  className?: string;
}

export const TextArea: React.FC<TextAreaProps> = ({
  name,
  placeholder = '',
  value,
  onChange,
  className,
}) => {
  return (
    <>
      <textarea
        name={name}
        id={name}
        placeholder={placeholder}
        value={value}
        onChange={onChange}
        className={`${className} border-border-color focus:outline-border h-32 w-full rounded-sm border px-3 py-2 focus:outline-1`}
      ></textarea>
    </>
  );
};
