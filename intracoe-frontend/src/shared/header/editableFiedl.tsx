import { InputText } from 'primereact/inputtext';
import { useState } from 'react';
import { FaCheck } from 'react-icons/fa6';
import { IoClose } from 'react-icons/io5';
import { CiEdit } from 'react-icons/ci';

interface Props {
  value: string;
  labelClass?: string;
  onSave: (newValue: string) => void;
}

export const EditableField: React.FC<Props> = ({
  value,
  labelClass = '',
  onSave,
}) => {
  const [isEditing, setIsEditing] = useState(false);
  const [tempValue, setTempValue] = useState(value);

  return (
    <div className="flex w-full items-center justify-center gap-2">
      {!isEditing ? (
        <>
          <p className={`text-center ${labelClass}`}>{value}</p>
          <CiEdit
            size={20}
            className="cursor-pointer"
            onClick={() => setIsEditing(true)}
          />
        </>
      ) : (
        <>
          <InputText
            value={tempValue}
            onChange={(e) => setTempValue(e.target.value)}
            className="w-full max-w-[200px] text-center"
            autoFocus
          />
          <button
            className="bg-primary-yellow rounded px-3 py-3 text-white"
            onClick={() => {
              onSave(tempValue);
              setIsEditing(false);
            }}
          >
            <FaCheck />
          </button>
          <button
            className="rounded bg-slate-500 px-3 py-3 text-white"
            onClick={() => {
              setTempValue(value);
              setIsEditing(false);
            }}
          >
            <IoClose />
          </button>
        </>
      )}
    </div>
  );
};
