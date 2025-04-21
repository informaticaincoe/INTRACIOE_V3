import React from 'react';

interface WhiteCardprops {
  children: React.ReactElement;
}

export const WhiteCard: React.FC<WhiteCardprops> = ({ children }) => {
  return <div className="flex-1 w-full rounded-md bg-white px-8 py-6">{children}</div>;
};
