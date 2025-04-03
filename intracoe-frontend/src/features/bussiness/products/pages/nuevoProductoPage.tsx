import { WhiteSectionsPage } from '../../../../shared/containers/whiteSectionsPage'
import { Title } from '../../../../shared/text/title'
import { StepperForm } from '../componentes/form/stepperFormContainer'

export const NuevoProductoPage = () => {
    return (
        <>
            <Title text="Nuevo producto" />
            <WhiteSectionsPage>
                <>
                    <StepperForm />
                </>
            </WhiteSectionsPage>
        </>
    )
}
