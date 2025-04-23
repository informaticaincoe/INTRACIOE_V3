import { HTMLProps } from 'react';

interface TitleProps {
  text: string;
  className?: HTMLProps<HTMLElement>['className'];
}

export const Title: React.FC<TitleProps> = ({ text, className = '' }) => {
  return <h1 className={`${className} text-3xl font-bold`}>{text}</h1>;
};
