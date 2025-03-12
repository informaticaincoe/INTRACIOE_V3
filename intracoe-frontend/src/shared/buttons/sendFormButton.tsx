import React from 'react';

interface SendFormButtonProps {
  text: string;
  onClick: (event: React.MouseEvent<HTMLButtonElement>) => void;
}

export const SendFormButton: React.FC<SendFormButtonProps> = ({
  text,
  onClick,
}) => {
  return (
    <button
      type="button"
      className="bg-primary-yellow mb-5 w-full rounded-md py-3 text-white"
      onClick={onClick}
    >
      {text}
    </button>
  );
};
