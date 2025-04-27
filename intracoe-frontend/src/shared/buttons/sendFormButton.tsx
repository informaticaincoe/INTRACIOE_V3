import React, { HTMLProps } from 'react';

interface SendFormButtonProps {
  text: string;
  onClick: (event: React.MouseEvent<HTMLButtonElement>) => void;
  className?: HTMLProps<HTMLElement>['className'];
}

export const SendFormButton: React.FC<SendFormButtonProps> = ({
  text,
  onClick,
  className,
}) => {
  return (
    <button
      type="button"
      className={`${className} rounded-md py-3 hover:cursor-pointer`}
      onClick={onClick}
    >
      {text}
    </button>
  );
};
