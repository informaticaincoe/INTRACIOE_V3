import { useEffect, useRef, useState } from 'react'
import { useNavigate, useParams } from 'react-router';
import { addMovimientoInventario, getMovimientosInventarioById, updateMovimientosInventarioById } from '../services/movimientoInventarioServices';
import { Almacen, ProductoResponse } from '../../../../shared/interfaces/interfaces';
import { Dropdown } from 'primereact/dropdown';
import { Title } from '../../../../shared/text/title';
import { getAllProducts } from '../../../../shared/services/productos/productosServices';
import { movimientoInterface } from '../interfaces/movimientoInvetarioInterface';
import { Input } from '../../../../shared/forms/input';
import { getAllAlmacenes } from '../../../../shared/services/tributos/tributos';
import { Calendar } from 'primereact/calendar';
import dayjs from 'dayjs';
import { CiCalendar } from 'react-icons/ci';
import { RadioButton } from 'primereact/radiobutton';
import CustomToast, { CustomToastRef, ToastSeverity } from '../../../../shared/toast/customToast';
import { FaCheckCircle } from 'react-icons/fa';
import { IoMdCloseCircle } from 'react-icons/io';

export const MovimientoInventarioEdit = () => {
  const [formData, setFormData] = useState<movimientoInterface>({
    almacen: 0,
    cantidad: 0,
    fecha: new Date(),
    id: 0,
    producto: 0,
    referencia: '',
    tipo: ''
  });

  const [productosLista, setProductosLista] = useState<ProductoResponse[]>([])
  const [almacenesLista, setAlmacenesLista] = useState<Almacen[]>([])
  let params = useParams();
  const toastRef = useRef<CustomToastRef>(null);
  const navigate = useNavigate();

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

  useEffect(() => {
    if (params.id)
      fetchDataEdit()

    fetchProducts()
    fetchAlmacenes()
  }, [])

  const fetchDataEdit = async () => {
    if (params.id) {
      try {
        const response = await getMovimientosInventarioById(params.id);

        if (response && response.id) {
          setFormData(response); 
        } else {
          // Si la respuesta no es válida, podemos establecer valores predeterminados
          setFormData({
            almacen: 0,
            cantidad: 0,
            fecha: new Date(),
            id: 0,
            producto: 0,
            referencia: '',
            tipo: ''
          });
        }

        console.log(response);
      } catch (error) {
        console.log(error);
      }
    }
  };


  const fetchProducts = async () => {
    try {
      const response = await getAllProducts()
      setProductosLista(response)
      console.log(response)
    } catch (error) {
      console.log(error)
    }
  }

  const fetchAlmacenes = async () => {
    try {
      const response = await getAllAlmacenes()
      setAlmacenesLista(response)
      console.log(response)
    } catch (error) {
      console.log(error)
    }
  }

  const handleChange = (e: any) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSendForm = async () => {
    // Convertir la fecha a formato ISO con zona horaria  
    const formattedDate = dayjs(formData.fecha).format('YYYY-MM-DDTHH:mm:ss.SSSSSS-06:00');

    const updatedFormData = { ...formData, fecha: formattedDate };

    if (params.id) {
      try {
        console.log(updatedFormData.fecha)
        const response = await updateMovimientosInventarioById(params.id, updatedFormData)
        console.log(response)
        handleAccion(
          'success',
          <FaCheckCircle size={38} />,
          'Movimiento de inventario actualizado con exito'
        );

        setTimeout(() => {
          // navigate('/movimiento-inventario/');
        }, 2000);
      } catch (error) {
        handleAccion(
          'error',
          <IoMdCloseCircle size={38} />,
          'Error al actualizar movimiento'
        );
      }
    }
    else {
      try {
        const response = await addMovimientoInventario(formData)
        console.log(response)
        handleAccion(
          'success',
          <FaCheckCircle size={38} />,
          'Movimiento de inventario creado con exito'
        );

        setTimeout(() => {
          navigate('/movimiento-inventario/');
        }, 2000);
      } catch (error) {
        handleAccion(
          'error',
          <IoMdCloseCircle size={38} />,
          'Error al crear movimiento'
        );
      }
    }
  }

  return (
    <>
      <CustomToast ref={toastRef} />

      <Title text={`${params.id ? ' Editar movimiento' : 'Nuevo movimiento'} `} />
      <div className='bg-white rounded-md p-10 my-10 mx-[20%]'>
        <>
          <form action="" className='flex flex-col gap-6'>
            <div className='flex gap-4'>
              <span className='flex flex-col text-start w-full'>
                <label htmlFor="producto">Producto</label>
                <Dropdown
                  name="producto"
                  value={formData?.producto}
                  onChange={(e) =>
                    handleChange({ target: { name: 'producto', value: e.value } })
                  }
                  options={productosLista}
                  optionLabel="descripcion"
                  optionValue="id"
                  placeholder="Seleccionar producto"
                  className="md:w-14rem w-full text-start"
                />
              </span>
              <span className='flex flex-col text-start'>
                <label htmlFor="producto">Cantidad</label>
                <Input type='number' name='cantidad' value={formData?.cantidad.toString()} onChange={handleChange} className='' />
              </span>
            </div>
            <div>
              <span className='flex flex-col text-start'>
                <label htmlFor="expiredDate">Fecha</label>

                <Calendar
                  name="fecha"
                  value={formData?.fecha ? dayjs(formData.fecha).toDate() : null} // Convertimos el valor a un objeto Date
                  onChange={handleChange}
                  dateFormat="dd-mm-yy" // Formato de fecha que desees
                  showIcon
                  showTime
                  icon={<CiCalendar size={20} color="rgba(0,0,0,0.5)" />}
                  iconPos="left"
                />

              </span>
            </div>
            <div>
              <span className='flex flex-col text-start w-full'>
                <label htmlFor="producto">Almacen</label>
                <Dropdown
                  name="almacen"
                  value={formData?.almacen}
                  onChange={(e) =>
                    handleChange({ target: { name: 'almacen', value: e.value } })
                  }
                  options={almacenesLista}
                  optionLabel="nombre"
                  optionValue="id"
                  placeholder="Seleccionar Almacen"
                  className="md:w-14rem w-full text-start"
                />
              </span>
            </div>
            <div>
              <span className='flex flex-col text-start w-full'>
                <label htmlFor="tipo">Tipo</label>
                <div className='flex gap-5'>
                  <div className="flex align-items-center">
                    <RadioButton
                      inputId="entrada"
                      name="tipo"
                      value="Entrada"
                      onChange={handleChange}
                      checked={formData?.tipo === 'Entrada'}
                    />
                    <label htmlFor="entrada" className="ml-2">Entrada</label>
                  </div>
                  <div className="flex align-items-center">
                    <RadioButton
                      inputId="salida"
                      name="tipo"
                      value="Salida"
                      onChange={handleChange}
                      checked={formData?.tipo === 'Salida'}
                    />
                    <label htmlFor="salida" className="ml-2">Salida</label>
                  </div>
                </div>
              </span>
            </div>
            <div className='text-start'>
              <label htmlFor="">Referencia</label>
              <Input name='referencia' value={formData?.referencia} onChange={handleChange} />
            </div>
          </form>

          <div className='w-full flex justify-start pt-5'>
            <button className='bg-primary-blue text-white rounded-md py-2 px-7' onClick={handleSendForm}>Guardar</button>
          </div>
        </>
      </div>
    </>
  )
}
