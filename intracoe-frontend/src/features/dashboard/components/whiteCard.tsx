import React from 'react'

interface WhiteCardprops {
    children: React.ReactElement
}

export const WhiteCard:React.FC<WhiteCardprops> = ({children}) => {
  return (
    <div className='bg-white rounded-md py-8 w-full px-10'>
        {children}
    </div>
  )
}
