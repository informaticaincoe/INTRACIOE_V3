import { SetStateAction, useEffect, useState } from 'react';
import { Title } from '../../../../shared/text/title';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';

import {
  getAllActivities,
  getAllAmbientes,
  getAllCondicioOperaciones,
  getAllDepartamentos,
  getAllDescuento,
  getAllIncoterms,
  getAllMetodosDePago,
  getAllTiposEstablecimientos,
  getAllModelosDeFacturacion,
  getAllMunicipios,
  getAllOtrosDocumentosAsociados,
  getAllPaises,
  getAllPlazos,
  getAllTipoContingencia,
  getAllTipoDocContingencia,
  getAllTipoDomicilioFiscal,
  getAllTipoDonacion,
  getAllTipoDTE,
  getAllTipoIdReceptor,
  getAllTipoInvalidacion,
  getAllTipoMoneda,
  getAllTipoPersona,
  getAllTipoRentencionIVA,
  getAllTipoServiciosMedicos,
  getAllTiposGeneracionDocumento,
  getAllTipoTransmision,
  getAllTipoTransporte,
  getPaisById,
  getDepartamentoById,
} from '../../../../shared/catalogos/services/catalogosServices';
import { HeaderTable } from '../components/headerTable';
// import { Paginator } from "primereact/paginator";
import { FaCheckCircle } from 'react-icons/fa';
import { EditModal } from '../../../../shared/modales/editModal';
import {
  updateActivity,
  updateAmbientes,
  updateCondicioOperaciones,
  updateDepartamentos,
  updateDescuento,
  updateIncoterms,
  updateMetodosDePago,
  updateModelosDeFacturacion,
  updateMunicipios,
  updateOtrosDocumentosAsociados,
  updatePaises,
  updatePlazos,
  updateTipoContingencia,
  updateTipoDocContingencia,
  updateTipoDomicilioFiscal,
  updateTipoDonacion,
  updateTipoDTE,
  updateTipoIdReceptor,
  updateTipoInvalidacion,
  updateTipoMoneda,
  updateTipoPersona,
  updateTipoServiciosMedicos,
  updateTiposEstablecimientos,
  updateTiposGeneracionDocumento,
  updateTipoTipoRentencionIVA,
  updateTipoTransmision,
  updateTipoTransporte,
} from '../../../../shared/catalogos/services/catalogosEditServices';
import { EditModalDescuento } from '../../../../shared/modales/editModalDescuento';
import {
  deleteAmbientes,
  deleteCondicioOperaciones,
  deleteDepartamentos,
  deleteDescuento,
  deleteIncoterms,
  deleteMetodosDePago,
  deleteModelosDeFacturacion,
  deleteMunicipios,
  deleteOtrosDocumentosAsociados,
  deletePaises,
  deletePlazos,
  deleteTipoContingencia,
  deleteTipoDocContingencia,
  deleteTipoDomicilioFiscal,
  deleteTipoDonacion,
  deleteTipoDTE,
  deleteTipoIdReceptor,
  deleteTipoInvalidacion,
  deleteTipoMoneda,
  deleteTipoPersona,
  deleteTipoRentencionIVA,
  deleteTipoServiciosMedicos,
  deleteTiposEstablecimientos,
  deleteTiposGeneracionDocumento,
  deleteTipoTransmision,
  deleteTipoTransporte,
} from '../../../../shared/catalogos/services/catalogosDeleteServices';
import { DeleteModal } from '../../../facturacion/activities/components/modales/deleteModal';
import {
  createAmbientes,
  createCondicioOperaciones,
  createDepartamentos,
  createDescuento,
  createIncoterms,
  createMetodosDePago,
  createModelosDeFacturacion,
  createMunicipios,
  createOtrosDocumentosAsociados,
  createPaises,
  createPlazos,
  createTipoContingencia,
  createTipoDocContingencia,
  createTipoDomicilioFiscal,
  createTipoDonacion,
  createTipoDTE,
  createTipoIdReceptor,
  createTipoInvalidacion,
  createTipoMoneda,
  createTipoPersona,
  createTipoRentencionIVA,
  createTipoServiciosMedicos,
  createTiposEstablecimientos,
  createTiposGeneracionDocumento,
  createTipoTransmision,
  createTipoTransporte,
} from '../../../../shared/catalogos/services/catalogoCreateServices';
import { NewActivityForm } from '../components/newActivityform';
import { NewModalDescuento } from '../components/newItemformDescuento';
import {
  createActivity,
  deleteActivity,
} from '../../../facturacion/activities/services/activitiesServices';
import { EditActivityForm } from '../components/editActivityForm';
import { Segmented } from 'antd';

type CatalogKey =
  | 'Actividades economicas'
  | 'Ambientes'
  | 'Modelo facturacion'
  | 'Tipo transmision'
  | 'Tipo contingencia'
  | 'Tipo retencion IVA'
  | 'Tipo generación de documento'
  | 'Tipo establecimiento'
  | 'Tipo servicio medico'
  | 'tipo documento tributario electronico'
  | 'Otros documentos asociados'
  | 'Tipo de identificacion receptores'
  | 'Paises'
  | 'Departamentos'
  | 'municipios'
  | 'Condiciones de operación'
  | 'Formas de pago'
  | 'Plazos de pago'
  | 'tipo de documento de contingencia'
  | 'Tipo de invalidación'
  | 'Tipo de donación'
  | 'Tipo de persona'
  | 'Tipo de transporte'
  | 'Incoterms'
  | 'Tipo de domicilio fiscal'
  | 'Tipo de moneda'
  | 'Descuento';

// Cada valor es una función que recibe opcionalmente un filtro y devuelve Promise<any[]>
const fetchers: Record<CatalogKey, (filter?: string) => Promise<any[]>> = {
  'Actividades economicas': (filter = '', page = 1, limit = 10) =>
    getAllActivities(page, limit, filter),
  'Ambientes': () => getAllAmbientes(),
  'Modelo facturacion': () => getAllModelosDeFacturacion(),
  'Tipo transmision': () => getAllTipoTransmision(),
  'Tipo contingencia': () => getAllTipoContingencia(),
  'Tipo retencion IVA': () => getAllTipoRentencionIVA(),
  'Tipo generación de documento': () => getAllTiposGeneracionDocumento(),
  'Tipo establecimiento': () => getAllTiposEstablecimientos(),
  'Tipo servicio medico': () => getAllTipoServiciosMedicos(),
  'tipo documento tributario electronico': () => getAllTipoDTE(),
  'Otros documentos asociados': () => getAllOtrosDocumentosAsociados(),
  'Tipo de identificacion receptores': () => getAllTipoIdReceptor(),
  'Paises': () => getAllPaises(),
  'Departamentos': () => getAllDepartamentos(),
  'municipios': () => getAllMunicipios(),
  'Condiciones de operación': () => getAllCondicioOperaciones(),
  'Formas de pago': () => getAllMetodosDePago(),
  'Plazos de pago': () => getAllPlazos(),
  'tipo de documento de contingencia': () => getAllTipoDocContingencia(),
  'Tipo de invalidación': () => getAllTipoInvalidacion(),
  'Tipo de donación': () => getAllTipoDonacion(),
  'Tipo de persona': () => getAllTipoPersona(),
  'Tipo de transporte': () => getAllTipoTransporte(),
  'Incoterms': () => getAllIncoterms(),
  'Tipo de domicilio fiscal': () => getAllTipoDomicilioFiscal(),
  'Tipo de moneda': () => getAllTipoMoneda(),
  'Descuento': () => getAllDescuento(),
};

const createFunctions: Record<CatalogKey, (body: any) => Promise<any>> = {
  'Actividades economicas': (body) => createActivity(body),
  'Ambientes': (body) => createAmbientes(body),
  'Modelo facturacion': (body) => createModelosDeFacturacion(body),
  'Tipo transmision': (body) => createTipoTransmision(body),
  'Tipo contingencia': (body) => createTipoContingencia(body),
  'Tipo retencion IVA': (body) => createTipoRentencionIVA(body),
  'Tipo generación de documento': (body) =>
    createTiposGeneracionDocumento(body),
  'Tipo establecimiento': (body) => createTiposEstablecimientos(body),
  'Tipo servicio medico': (body) => createTipoServiciosMedicos(body),
  'tipo documento tributario electronico': (body) => createTipoDTE(body),
  'Otros documentos asociados': (body) => createOtrosDocumentosAsociados(body),
  'Tipo de identificacion receptores': (body) => createTipoIdReceptor(body),
  'Paises': (body) => createPaises(body),
  'Departamentos': (body) => createDepartamentos(body),
  'municipios': (body) => createMunicipios(body),
  'Condiciones de operación': (body) => createCondicioOperaciones(body),
  'Formas de pago': (body) => createMetodosDePago(body),
  'Plazos de pago': (body) => createPlazos(body),
  'tipo de documento de contingencia': (body) =>
    createTipoDocContingencia(body),
  'Tipo de invalidación': (body) => createTipoInvalidacion(body),
  'Tipo de donación': (body) => createTipoDonacion(body),
  'Tipo de persona': (body) => createTipoPersona(body),
  'Tipo de transporte': (body) => createTipoTransporte(body),
  'Incoterms': (body) => createIncoterms(body),
  'Tipo de domicilio fiscal': (body) => createTipoDomicilioFiscal(body),
  'Tipo de moneda': (body) => createTipoMoneda(body),
  'Descuento': (body) => createDescuento(body),
};

const deleteFunctions: Record<CatalogKey, (id: number) => Promise<any>> = {
  'Actividades economicas': (id) => deleteActivity(id),
  'Ambientes': (id) => deleteAmbientes(id),
  'Modelo facturacion': (id) => deleteModelosDeFacturacion(id),
  'Tipo transmision': (id) => deleteTipoTransmision(id),
  'Tipo contingencia': (id) => deleteTipoContingencia(id),
  'Tipo retencion IVA': (id) => deleteTipoRentencionIVA(id),
  'Tipo generación de documento': (id) => deleteTiposGeneracionDocumento(id),
  'Tipo establecimiento': (id) => deleteTiposEstablecimientos(id),
  'Tipo servicio medico': (id) => deleteTipoServiciosMedicos(id),
  'tipo documento tributario electronico': (id) => deleteTipoDTE(id),
  'Otros documentos asociados': (id) => deleteOtrosDocumentosAsociados(id),
  'Tipo de identificacion receptores': (id) => deleteTipoIdReceptor(id),
  'Paises': (id) => deletePaises(id),
  'Departamentos': (id) => deleteDepartamentos(id),
  'municipios': (id) => deleteMunicipios(id),
  'Condiciones de operación': (id) => deleteCondicioOperaciones(id),
  'Formas de pago': (id) => deleteMetodosDePago(id),
  'Plazos de pago': (id) => deletePlazos(id),
  'tipo de documento de contingencia': (id) => deleteTipoDocContingencia(id),
  'Tipo de invalidación': (id) => deleteTipoInvalidacion(id),
  'Tipo de donación': (id) => deleteTipoDonacion(id),
  'Tipo de persona': (id) => deleteTipoPersona(id),
  'Tipo de transporte': (id) => deleteTipoTransporte(id),
  'Incoterms': (id) => deleteIncoterms(id),
  'Tipo de domicilio fiscal': (id) => deleteTipoDomicilioFiscal(id),
  'Tipo de moneda': (id) => deleteTipoMoneda(id),
  'Descuento': (id) => deleteDescuento(id),
};

const editFunctions: Record<CatalogKey, (id: any, data: any) => Promise<any>> =
{
  'Actividades economicas': (id, data) => updateActivity(id, data),
  'Ambientes': (id, data) => updateAmbientes(id, data),
  'Modelo facturacion': (id, data) => updateModelosDeFacturacion(id, data),
  'Tipo transmision': (id, data) => updateTipoTransmision(id, data),
  'Tipo contingencia': (id, data) => updateTipoContingencia(id, data),
  'Tipo retencion IVA': (id, data) => updateTipoTipoRentencionIVA(id, data),
  'Tipo generación de documento': (id, data) =>
    updateTiposGeneracionDocumento(id, data),
  'Tipo establecimiento': (id, data) => updateTiposEstablecimientos(id, data),
  'Tipo servicio medico': (id, data) => updateTipoServiciosMedicos(id, data),
  'tipo documento tributario electronico': (id, data) =>
    updateTipoDTE(id, data),
  'Otros documentos asociados': (id, data) =>
    updateOtrosDocumentosAsociados(id, data),
  'Tipo de identificacion receptores': (id, data) =>
    updateTipoIdReceptor(id, data),
  'Paises': (id, data) => updatePaises(id, data),
  'Departamentos': (id, data) => updateDepartamentos(id, data),
  'municipios': (id, data) => updateMunicipios(id, data),
  'Condiciones de operación': (id, data) =>
    updateCondicioOperaciones(id, data),
  'Formas de pago': (id, data) => updateMetodosDePago(id, data),
  'Plazos de pago': (id, data) => updatePlazos(id, data),
  'tipo de documento de contingencia': (id, data) =>
    updateTipoDocContingencia(id, data),
  'Tipo de invalidación': (id, data) => updateTipoInvalidacion(id, data),
  'Tipo de donación': (id, data) => updateTipoDonacion(id, data),
  'Tipo de persona': (id, data) => updateTipoPersona(id, data),
  'Tipo de transporte': (id, data) => updateTipoTransporte(id, data),
  'Incoterms': (id, data) => updateIncoterms(id, data),
  'Tipo de domicilio fiscal': (id, data) =>
    updateTipoDomicilioFiscal(id, data),
  'Tipo de moneda': (id, data) => updateTipoMoneda(id, data),
  'Descuento': (id, data) => updateDescuento(id, data),
};

export const CatalogosPage = () => {
  const [selectedCatalog, setSelectedCatalog] = useState<CatalogKey>(
    'Actividades economicas'
  );
  const [filterTerm, setFilterTerm] = useState<string>('');
  const [data, setData] = useState<any[]>([]);
  const [loading, setLoading] = useState<boolean>(false);

  const [auxSelectedItem, setAuxSelectedRows] = useState<any[]>([]); //para almacenar los filas seleccionadas
  const [rowClick] = useState<boolean>(true); //detectar una fila selecionada

  const [isEditModalVisible, setEditModalVisible] = useState(false); //mostrar modal de editar
  const [editItem, setEditItem] = useState<any | null>(null); // item a editar
  const [isDeleteModalVisible, setDeleteModalVisible] = useState(false);
  const [deleteItem, setDeleteItem] = useState<any | null>(null);
  const [showModalNew, setShowModalNew] = useState(false);

  // const [pagination, setPagination] = useState<pagination>({
  //   current_page: 1,
  //   page_size: 1,
  //   total_pages: 1,
  //   total_records: 1,
  // });

  useEffect(() => {
    //renderizar lista de datos
    fetchData();
  }, [selectedCatalog, filterTerm, showModalNew]);

  const fetchData = async () => {
    setLoading(true);
    try {
      // Llamamos al fetcher correspondiente, pasándole filterTerm
      const result = await fetchers[selectedCatalog](filterTerm);

      if (selectedCatalog === 'Departamentos') {
        const departamentosConPais = await Promise.all(
          result.map(async (departamento) => {
            const paisData = await getPaisById(departamento.pais);
            console.log("pdpdppdpdpd", paisData)
            return {
              ...departamento,
              pais: {
                id: departamento.pais,
                descripcion: paisData
              },
            };
          })
        );
        setData(departamentosConPais);
        console.log("departamentosConPais:", departamentosConPais)
      } else if (selectedCatalog === 'municipios') {
        const municipiosConDepartamento = await Promise.all(
          result.map(async (municipio) => {
            const depData = await getDepartamentoById(municipio.departamento);
            return {
              ...municipio,
              departamento: {
                id: municipio.departamento,
                descripcion: depData.descripcion,
              },
            };
          })
        );
        setData(municipiosConDepartamento);
        console.log("municipiosConDepartamento:", municipiosConDepartamento)

      } else {
        setData(result);
      }

    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteClick = () => {
    if (!auxSelectedItem.length) return;
    setDeleteItem(auxSelectedItem[0]);
    setDeleteModalVisible(true);
  };

  // cuando el usuario clickea en Editar:
  const handleEdit = () => {
    console.log(auxSelectedItem[0]);
    if (auxSelectedItem.length !== 1) return;
    setEditItem(auxSelectedItem[0]);
    console.log(EditModal);
    setEditModalVisible(true);
  };

  // callback tras guardar en el modal:
  const onSaveFromModal = async () => {
    await fetchData();
    setAuxSelectedRows([]);
    setEditModalVisible(false);
    setShowModalNew(false);
  };

  // Genera columnas dinámicamente
  const columns = data.length
    ? Object.keys(data[0]).map((field) => ({
      field,
      header: field.toUpperCase(),
    }))
    : [];

  return (
    <>
      <Title text="Catálogos" />
      <div className="grid h-[80vh] grid-cols-[20%_80%] gap-10 overflow-hidden p-10">
        {/* Sidebar */}
        <div
          id="catalogos-list"
          className="max-h-[80vh] overflow-y-auto rounded-md bg-white"
        >
          <span className="flex w-full flex-col p-4">
            <h2 className="sticky top-0 bg-white pt-4 pb-4 text-xl font-semibold">
              Lista catálogos
            </h2>
            <ul className="flex flex-col gap-2 text-start">
              {(
                [
                  'Actividades economicas',
                  'Ambientes',
                  'Modelo facturacion',
                  'Tipo transmision',
                  'Tipo contingencia',
                  'Tipo retencion IVA',
                  'Tipo generación de documento',
                  'Tipo establecimiento',
                  'Tipo servicio medico',
                  'tipo documento tributario electronico',
                  'Otros documentos asociados',
                  'Tipo de identificacion receptores',
                  'Paises',
                  'Departamentos',
                  'municipios',
                  'Condiciones de operación',
                  'Formas de pago',
                  'Plazos de pago',
                  'tipo de documento de contingencia',
                  'Tipo de invalidación',
                  'Tipo de donación',
                  'Tipo de persona',
                  'Tipo de transporte',
                  'Incoterms',
                  'Tipo de domicilio fiscal',
                  'Tipo de moneda',
                  'Descuento',
                ] as CatalogKey[]
              ).map((key) => (
                <li
                  key={key}
                  onClick={() => {
                    setSelectedCatalog(key);
                    setAuxSelectedRows([]);
                  }}
                  className={
                    `cursor-pointer rounded-md px-2 py-2 ` +
                    (selectedCatalog === key
                      ? 'text-primary-blue bg-blue-200'
                      : 'hover:bg-blue-100')
                  }
                >
                  {key.charAt(0).toUpperCase() + key.slice(1)}
                </li>
              ))}
            </ul>
          </span>
        </div>
        {/* Contenido */}
        <div className="bg-white p-5">
          {loading ? (
            <p>Cargando...</p>
          ) : (
            <>
              <HeaderTable
                nombre={selectedCatalog}
                filterTerm={filterTerm}
                setFilterTerm={setFilterTerm}
                setShowModalNew={setShowModalNew}
              />
              {auxSelectedItem.length > 0 && ( // Verificar si hay productos seleccionados
                <div className="my-5 flex justify-between rounded bg-blue-50 p-5">
                  <p className="text-blue flex items-center gap-2">
                    <FaCheckCircle className="" />
                    items seleccionados {auxSelectedItem.length}
                  </p>
                  <span className="flex gap-2">
                    {auxSelectedItem.length === 1 && (
                      <span
                        className="border-blue flex items-center gap-2 rounded-md border px-3 py-1 hover:cursor-pointer"
                        onClick={handleEdit}
                      >
                        <p className="text-blue">Editar</p>
                      </span>
                    )}
                    {
                      <button
                        className="border-red flex items-center gap-2 rounded-md border px-3 py-1 hover:cursor-pointer"
                        onClick={handleDeleteClick}
                      >
                        <p className="text-red">Eliminar</p>
                      </button>
                    }
                  </span>
                </div>
              )}
              <DataTable
                value={data}
                responsiveLayout="scroll"
                selectionMode={rowClick ? null : 'multiple'}
                selection={auxSelectedItem!}
                onSelectionChange={(e: { value: SetStateAction<any[]> }) =>
                  setAuxSelectedRows(e.value)
                }
                paginator
                rows={5}
                rowsPerPageOptions={[5, 10, 25, 50]}
              >
                <Column
                  selectionMode="multiple"
                  headerStyle={{ width: '3rem' }}
                ></Column>

                {columns.map((col) => {

                  return (
                    col.header !== 'ID' && (
                      <Column
                        key={col.field}
                        field={col.field}
                        header={col.header}
                        body={(rowData) => {
                          const value = rowData[col.field];
                          if (typeof value === 'object' && value !== null) {
                            return value.descripcion || JSON.stringify(value);
                          }
                          return value;
                        }}
                      />
                    )
                  )
                })}
              </DataTable>
            </>
          )}
        </div>

        {editItem && selectedCatalog != 'Descuento' && (
          <EditActivityForm
            item={editItem}
            catalogo={selectedCatalog}
            visible={isEditModalVisible}
            setVisible={setEditModalVisible}
            onSave={onSaveFromModal}
            saveFunction={(id: number, data: any) =>
              editFunctions[selectedCatalog](id, data)
            }
          />
        )}

        {editItem && selectedCatalog == 'Descuento' && (
          <EditModalDescuento
            activity={editItem}
            visible={isEditModalVisible}
            setVisible={setEditModalVisible}
            onSave={onSaveFromModal}
            saveFunction={(id, data) =>
              editFunctions[selectedCatalog](id, data)
            }
          />
        )}

        {deleteItem && (
          <DeleteModal
            item={deleteItem}
            visible={isDeleteModalVisible}
            setVisible={setDeleteModalVisible}
            deleteFunction={(id) => deleteFunctions[selectedCatalog](id)}
            onDeleted={async () => {
              await fetchData();
              setAuxSelectedRows([]);
            }}
          />
        )}

        {showModalNew && selectedCatalog != 'Descuento' && (
          <NewActivityForm
            catalogo={selectedCatalog}
            visible={showModalNew}
            setVisible={setShowModalNew}
            createFunction={createFunctions[selectedCatalog]}
          />
        )}

        {showModalNew && selectedCatalog == 'Descuento' && (
          <NewModalDescuento
            onSave={onSaveFromModal}
            visible={showModalNew}
            setVisible={setShowModalNew}
            createFunction={createFunctions[selectedCatalog]}
          />
        )}

        {/* <div className="pt-5">
          <Paginator
            first={(pagination.current_page - 1) * pagination.page_size}
            rows={pagination.page_size}
            totalRecords={pagination.total_records}
            rowsPerPageOptions={[10, 25, 50]}
            onPageChange={onPageChange}
          />
        </div> */}
      </div>
    </>
  );
};
