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
    <div className={`m-14 rounded-md bg-white px-10 py-5 ${className}`}>
      {children}
    </div>
  );
};
