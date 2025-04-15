import React from 'react'

interface WhiteCardprops {
    children: React.ReactElement
}

export const WhiteCard:React.FC<WhiteCardprops> = ({children}) => {
  return (
    <div className='bg-white rounded-md py-6 w-full px-8'>
        {children}
    </div>
  )
}
