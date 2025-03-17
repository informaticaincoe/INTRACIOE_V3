import { HTMLProps } from 'react';

interface WhiteSectionPageProps {
  children: React.ReactElement;
  className?: HTMLProps<HTMLElement>['className'];
}

export const WhiteSectionsPage: React.FC<WhiteSectionPageProps> = ({
  children,
  className,
}) => {
  return (
    <div className={`m-10 bg-white px-10 py-5 rounded-md ${className}`}>{children}</div>
  );
};
