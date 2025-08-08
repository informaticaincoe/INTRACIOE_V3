import { Checkbox } from 'primereact/checkbox';
import React, { useEffect, useState } from 'react';
import { Input } from '../../../../../../shared/forms/input';
import { OtrosDocumentosAsociados } from '../../../../../../shared/interfaces/interfaces';
import { Dialog } from 'primereact/dialog';
import {
    getAllOtrosDocumentosAsociados,
    getAllTipoTransporte,
} from '../../../../../../shared/catalogos/services/catalogosServices';
import { Dropdown } from 'primereact/dropdown';

interface CheckboxDocumentosAsociados {
    tieneDocumentoAsociado: boolean;
    setTieneDocumentoAsociado: any;
    setFormDataDocumentosAsociados: any;
    formDataDocumentosAsociados: Partial<OtrosDocumentosAsociados>;
    setDocumentosAsociadosLista: any;
    documentosAsociadosLista: OtrosDocumentosAsociados[];
}

export const CheckboxDocumentosAsociados: React.FC<CheckboxDocumentosAsociados> = ({
    tieneDocumentoAsociado,
    setTieneDocumentoAsociado,
    setFormDataDocumentosAsociados,
    formDataDocumentosAsociados,
    documentosAsociadosLista,
    setDocumentosAsociadosLista,
}) => {
    const [visible, setVisible] = useState(false);
    const [tipoDocAsociadoLista, setTipoDocAsociadoLista] = useState<any[]>();
    const [tipoTransporteLista, setTipoTransporteLista] = useState<any[]>();

    useEffect(() => {
        fetchTipoDocAsociados();
        fetchModoTransporte();
    }, []);

    useEffect(() => {
        if (visible == false)
            setFormDataDocumentosAsociados({
                codDocAsociado: null,
                descDocumento: null,
                detalleDocumento: null,
                modoTransp: null,
                placaTrans: null,
                numConductor: null,
                nombreConductor: null,
            });
    }, [visible]);

    const fetchTipoDocAsociados = async () => {
        try {
            const response = await getAllOtrosDocumentosAsociados();
            setTipoDocAsociadoLista(response);
        } catch (error) {
            console.log('Error doc asociado', error);
        }
    };

    const fetchModoTransporte = async () => {
        try {
            const response = await getAllTipoTransporte();
            setTipoTransporteLista(response);
        } catch (error) {
            console.log('Error doc asociado', error);
        }
    };

    const handleChange = (e: any) => {
        setFormDataDocumentosAsociados({
            ...formDataDocumentosAsociados,
            [e.target.name]: e.target.value,
        });
    };

    useEffect(() => {
        console.log("formDataDocumentosAsociados",formDataDocumentosAsociados)
    }, [formDataDocumentosAsociados])

    const addNuevoDocumentoAsociado = (e: any) => {
        setTieneDocumentoAsociado(e.checked ?? false);
        if (documentosAsociadosLista.length == 0) {
            setVisible(true);
        }
    };

    const sendForm = (e: React.FormEvent) => {
        e.preventDefault();

        if (!formDataDocumentosAsociados.codDocAsociado) {
            console.warn('Debe seleccionar un documento asociado');
            return;
        }

        const doc = formDataDocumentosAsociados.codDocAsociado;

        const nuevoDoc = {
            ...formDataDocumentosAsociados,
            codDocAsociado: doc.codigo,
            nombreDocAsociado: doc.descripcion,
            id: doc.id,
        };

        setDocumentosAsociadosLista((prevLista: any) => [...prevLista, nuevoDoc]);
        setVisible(false);

        setFormDataDocumentosAsociados({
            codDocAsociado: null,
            descDocumento: '',
            detalleDocumento: '',
            modoTransp: '',
            placaTrans: '',
            numConductor: '',
            nombreConductor: '',
        });
    };

    return (
        <div>
            <div className="flex justify-between items-center pb-5">
                <div className=" flex gap-3">
                    <Checkbox
                        inputId="documento-asociados"
                        onChange={(e) => addNuevoDocumentoAsociado(e)}
                        checked={tieneDocumentoAsociado}
                    />
                    <label htmlFor="documento-asociados">Contiene documentos asociados</label>
                </div>
                {tieneDocumentoAsociado && (
                    <button
                        className="border border-primary-blue bg-white text-primary-blue rounded-md px-7 py-3 hover:bg-primary-blue hover:text-white"
                        onClick={() => setVisible(true)}
                    >
                        Agregar documento
                    </button>
                )}
            </div>

            <Dialog
                header="Nuevo documento asociado"
                style={{ width: '50%' }}
                visible={visible}
                onHide={() => {
                    if (!visible) return;
                    setVisible(false);
                    if (documentosAsociadosLista.length == 0) setTieneDocumentoAsociado(false);
                }}
            >
                <form className="text-start rounded-md 510 py-5 flex flex-col gap-4" onSubmit={sendForm}>
                    <span>
                        <label>Documento asociado</label>
                        <Dropdown
                            value={formDataDocumentosAsociados.codDocAsociado}
                            onChange={(e) =>
                                handleChange({
                                    target: { name: 'codDocAsociado', value: e.value },
                                })
                            }
                            options={tipoDocAsociadoLista}
                            optionLabel="descripcion"
                            placeholder="Seleccione un tipo de documento asociado"
                            className="w-full md:w-14rem"
                        />
                    </span>

                    {(formDataDocumentosAsociados.codDocAsociado?.codigo == "1" ||
                        formDataDocumentosAsociados.codDocAsociado?.codigo == "2") && (
                            <>
                                <span>
                                    <label>Identificación del documento asociado</label>
                                    <Input name="descDocumento" value={formDataDocumentosAsociados.descDocumento} onChange={handleChange} />
                                </span>
                                <span>
                                    <label>Descripción de documento asociado</label>
                                    <Input name="detalleDocumento" value={formDataDocumentosAsociados.detalleDocumento} onChange={handleChange} />
                                </span>
                            </>
                        )}

                    {formDataDocumentosAsociados.codDocAsociado?.codigo == "4" && (
                        <>
                            <span>
                                <label>Modo de transporte</label>
                                <Dropdown
                                    value={formDataDocumentosAsociados.modoTransp}
                                    onChange={(e) => handleChange({ target: { name: 'modoTransp', value: e.value } })}
                                    options={tipoTransporteLista}
                                    optionLabel="descripcion"
                                    optionValue="codigo"
                                    placeholder="Seleccione un tipo de transporte"
                                    className="w-full md:w-14rem"
                                />
                            </span>
                            <span>
                                <label>Número de identificación del transporte</label>
                                <Input name="placaTrans" value={formDataDocumentosAsociados.placaTrans} onChange={handleChange} />
                            </span>
                            <span>
                                <label>Número de identificación del conductor</label>
                                <Input name="numConductor" value={formDataDocumentosAsociados.numConductor} onChange={handleChange} />
                            </span>
                            <span>
                                <label>Nombre y apellidos del conductor</label>
                                <Input name="nombreConductor" value={formDataDocumentosAsociados.nombreConductor} onChange={handleChange} />
                            </span>
                        </>
                    )}
                    <button type="submit" className="rounded self-end bg-primary-blue text-white px-5 py-2">
                        Agregar documento
                    </button>
                </form>
            </Dialog>
        </div>
    );
};
