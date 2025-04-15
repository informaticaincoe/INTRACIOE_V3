import { Button } from 'primereact/button';
import React, { HTMLProps } from 'react';

interface IconButton {
  text: string;
  icon: React.ReactElement;
  className?: HTMLProps<HTMLElement>['className'];
  onClick?: (event: React.MouseEvent<HTMLButtonElement>) => void;
}

export const IconButton: React.FC<IconButton> = ({
  text,
  icon,
  className,
  onClick,
}) => {
  return (
    <Button
      size="large"
      icon={icon}
      unstyled
      pt={{
        root: {
          className: `${className} cursor-pointer text-white px-3 py-2 border-round border-none flex gap-2 rounded-sm`,
        },
        label: { className: 'text-white font-bold text-xl' },
      }}
      onClick={onClick}
    >
      <p className="pr-3 text-sm">{text}</p>
    </Button>
  );
};
