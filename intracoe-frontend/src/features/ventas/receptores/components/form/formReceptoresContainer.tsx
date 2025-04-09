import React, { useEffect, useRef, useState } from 'react'
import { useNavigate, useParams } from 'react-router';
import { ReceptorRequestDefault, ReceptorRequestInterface } from '../../../../../shared/interfaces/interfaces';
import CustomToast, { CustomToastRef, ToastSeverity } from '../../../../../shared/toast/customToast';
import { WhiteSectionsPage } from '../../../../../shared/containers/whiteSectionsPage';
import { Steps } from 'antd';
import { StepperInformacionGeneralReceptor } from './stepperInformacionGeneralReceptor';
import { StepperFormInfoContactoReceptor } from './stepperFormInfoContactoReceptor';
import { Title } from '../../../../../shared/text/title';
import { createReceptor, editReceptor, getReceptorById } from '../../../../../shared/services/receptor/receptorServices';

export const FormReceptoresContainer = () => {
    let params = useParams()

    // Estado para controlar el paso actual
    const [current, setCurrent] = useState(0);
    const [formData, setFormData] = useState<ReceptorRequestInterface>(ReceptorRequestDefault);
    const toastRef = useRef<CustomToastRef>(null);
    const navigate = useNavigate()

    useEffect(() => {
        if (params.id)
            fetchReceptorEdit()
    }, [])

    const fetchReceptorEdit = async () => {
        try {
            if (params.id) {
                const data = await getReceptorById(params.id)
                console.log(data)
                setFormData(data)
            }
        } catch (error) {
            console.log(error)
        }
    }

    const handleAccion = (
        severity: ToastSeverity,
        icon: any,
        summary: string
    ) => {
        toastRef.current?.show({
            severity: severity,
            summary: summary,
            icon: icon,
            life: 2000,
        });
    };

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSendForm = async (e: React.FormEvent) => {
        e.preventDefault();

        console.log(formData)
        if (params.id) {
            try {
                const response = await editReceptor(params.id, formData);
                console.log(response);
            } catch (error) {
                console.log(error);
            }
        }
        else {
            try {
                const response = await createReceptor(formData);
                console.log(response);
            } catch (error) {
                console.log(error);
            }
        }
    };

    const steps = [
        {
            title: 'Información general',
            content: (
                <>
                    <div>
                        <StepperInformacionGeneralReceptor
                            formData={formData}
                            handleChange={handleChange}
                        />
                    </div>
                    <div className="justify-content-end flex pt-4">
                        <button
                            onClick={() => setCurrent(current + 1)}
                            className="bg-primary-blue rounded-md px-6 py-3 text-white"
                        >
                            Siguiente
                        </button>
                    </div>
                </>
            ),
        },
        {
            title: 'Informacion de contacto',
            content: (
                <>
                    <StepperFormInfoContactoReceptor
                        formData={formData}
                        handleChange={handleChange}
                    />
                    <div className="flex w-full justify-between pt-4">
                        <button
                            onClick={() => setCurrent(current - 1)}
                            className="border-gray text-gray rounded-md border px-10 py-3"
                        >
                            Atras
                        </button>
                        <button
                            className="bg-primary-yellow rounded-md px-6 py-3 text-white"
                            onClick={handleSendForm}
                        >
                            Guardar
                        </button>
                    </div>
                </>
            ),
        },
    ];

    return (
        <>
            <Title text="Nuevo receptor" />
            <WhiteSectionsPage className="mx-[10%] px-[5%] py-[3%]">
                <>
                    <Steps
                        current={current}
                        items={steps.map((item) => ({ key: item.title, title: item.title }))}
                        style={{ marginBottom: '5%' }}
                    />
                    <div style={{ marginTop: 24 }}>{steps[current].content}</div>
                    <CustomToast ref={toastRef} />
                </>
            </WhiteSectionsPage>
        </>
    );
};
