import { Checkbox } from 'primereact/checkbox';
import React from 'react';

interface BaseImponibleProps {
  baseImponible: boolean;
  setBaseImponible: any;
}

export const CheckboxBaseImponible: React.FC<BaseImponibleProps> = ({
  baseImponible,
  setBaseImponible,
}) => {
  return (
    <>
      <div className="flex gap-3 text-start">
        <Checkbox
          inputId="baseImponible"
          onChange={(e) => setBaseImponible(e.checked ?? false)}
          checked={baseImponible}
        ></Checkbox>
        <label htmlFor="baseImponible" className="opacity-70">
          Base Imponible
        </label>
      </div>
    </>
  );
};
