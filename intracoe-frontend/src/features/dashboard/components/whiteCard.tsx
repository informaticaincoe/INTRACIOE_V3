import React from 'react';

interface WhiteCardprops {
  children: React.ReactElement;
}

export const WhiteCard: React.FC<WhiteCardprops> = ({ children }) => {
  return (
    <div className="w-full flex-1 rounded-md bg-white px-8 py-6">
      {children}
    </div>
  );
};
