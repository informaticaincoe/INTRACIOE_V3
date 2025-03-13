interface WhiteSectionPageProps {
    children: React.ReactElement
}

export const WhiteSectionsPage:React.FC<WhiteSectionPageProps> =( { children } )=>{
    return(
        <div className="m-10 bg-white px-10 py-5">
            {children}
        </div>
    )
}