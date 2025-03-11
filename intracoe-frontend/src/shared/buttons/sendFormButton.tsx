import React from "react";

interface SendFormButtonProps{
    text: string;
    onClick: (event: React.MouseEvent<HTMLButtonElement>) => void
}

export const SendFormButton:React.FC<SendFormButtonProps> = ({text, onClick}) => {
  return (
    <button
        type="button"
        className="bg-primary-yellow w-full py-3 text-white mb-5 rounded-md"
        onClick={onClick}
      >
        {text}
      </button>
  )
}
