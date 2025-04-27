// import { useState } from "react";
import {
  Impuesto,
  ProductoRequest,
  Tributos,
} from '../../../../../shared/interfaces/interfaces';
import { Input } from '../../../../../shared/forms/input';
import { Checkbox } from 'primereact/checkbox';
import { useEffect, useState } from 'react';
import { getAllTributos } from '../../../../../shared/services/tributos/tributos';
import { Dropdown } from 'primereact/dropdown';
import { getAllImpuestos } from '../../../../../shared/services/productos/productosServices';
import { MultiSelect } from 'primereact/multiselect';

interface StepperInformacionGeneralProps {
  formData: ProductoRequest;
  handleChange: any;
}

export const StepperFormImpuestoStock: React.FC<
  StepperInformacionGeneralProps
> = ({ formData, handleChange }) => {
  const [tributo, setTributo] = useState<Tributos[]>([]);
  const [impuestos, setImpuestos] = useState<Impuesto[]>([]);

  useEffect(() => {
    fetchTributos();
    fetchImpuestos();
  }, []);

  const fetchTributos = async () => {
    try {
      const response = await getAllTributos();
      setTributo(response);
    } catch (error) {
      console.log(error);
    }
  };

  const fetchImpuestos = async () => {
    try {
      const response = await getAllImpuestos();
      setImpuestos(response);
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <>
      <div className="flex flex-col gap-10">
        <div className="flex w-full gap-5">
          <span className="w-full">
            <label htmlFor="tipo_documento" className="flex">
              <span className="text-red pr-1">*</span> Stock:
            </label>
            <Input
              type="number"
              name="stock"
              value={formData.stock.toString()}
              onChange={handleChange}
            />
          </span>
          <span className="w-full">
            <label htmlFor="tipo_documento" className="flex">
              <span className="text-red pr-1">*</span> Stock minimo:
            </label>
            <Input
              type="number"
              name="stock_minimo"
              value={formData.stock_minimo.toString()}
              onChange={handleChange}
            />
          </span>
          <span className="w-full">
            <label htmlFor="tipo_documento" className="flex">
              <span className="text-red pr-1">*</span> Stock maximo
            </label>
            <Input
              type="number"
              name="stock_maximo"
              value={formData.stock_maximo.toString()}
              onChange={handleChange}
            />
          </span>
        </div>
        <span className="w-full">
          <label htmlFor="tipo_documento" className="flex">
            <span className="text-red pr-1">*</span> Impuestos
          </label>
          <MultiSelect
            name="impuestos"
            value={formData.impuestos}
            onChange={(e) =>
              handleChange({ target: { name: 'impuestos', value: e.value } })
            }
            options={impuestos}
            itemTemplate={(option) => (
              <p>
                {option.nombre} - {option.porcentaje}
              </p>
            )}
            optionValue="id"
            selectedItemTemplate={(id: number) => {
              // lookup the full object by id
              const opt = impuestos.find((i) => i.id === id);
              return opt ? (
                <div className="flex items-center gap-1">
                  <span>{opt.nombre}</span>
                  <span>– {opt.porcentaje}</span>
                </div>
              ) : null;
            }}
            placeholder="Seleccionar el tipo de item"
            className="flex w-full justify-between rounded-md border text-start"
          />
        </span>
        <span className="w-full">
          <label htmlFor="tipo_documento" className="flex">
            <span className="text-red pr-1">*</span> Referencia interna
          </label>
          <Input
            type="text"
            name="referencia_interna"
            value={formData.referencia_interna ?? ''}
            onChange={handleChange}
          />
        </span>
        <span className="w-full">
          <label htmlFor="tipo_documento" className="flex">
            <span className="text-red pr-1">*</span> Tributo
          </label>
          <Dropdown
            name="tributo"
            value={formData.tributo}
            onChange={(e) =>
              handleChange({ target: { name: 'tributo', value: e.value } })
            }
            options={tributo}
            optionLabel="descripcion"
            optionValue="id"
            placeholder="Seleccionar el tipo de item"
            className="md:w-14rem w-full text-start"
          />
        </span>
        <span className="flex w-full">
          <Checkbox
            onChange={(e) =>
              handleChange({ target: { name: 'precio_iva', value: e.checked } })
            }
            checked={formData.precio_iva}
          />
          <label htmlFor="precio_iva" className="flex pl-2">
            Precio Iva
          </label>
        </span>
      </div>
    </>
  );
};
