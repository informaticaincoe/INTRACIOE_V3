import { Checkbox } from 'primereact/checkbox';
import { useState } from 'react';
import { Input } from '../../../../../../../shared/forms/input';

export const CheckBoxVentaTerceros = () => {
  const [checked, setChecked] = useState<boolean>(false);

  const [formData, setFormData] = useState({
    nitTercero: '',
    razonSocialTercero: '',
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  return (
    <>
      <div className="flex gap-3 text-start">
        <Checkbox
          inputId="VentaTerceros"
          onChange={(e) => setChecked(e.checked ?? false)}
          checked={checked}
        ></Checkbox>
        <label htmlFor="VentaTerceros" className="opacity-70">
          Venta a cuenta de terceros
        </label>
      </div>
      {checked && (
        <div className="flex flex-col gap-5 text-start">
          <span>
            <label htmlFor="nitTercero" className="opacity-70">
              NIT de tercero
            </label>
            <Input
              name="nitTercero"
              placeholder=""
              type="text"
              value={formData.nitTercero}
              onChange={handleChange}
            />
          </span>
          <span>
            <label htmlFor="razonSocialTercero" className="opacity-70">
              Nombre o razón social de tercero
            </label>
            <Input
              name="razonSocialTercero"
              placeholder=""
              type="text"
              value={formData.razonSocialTercero}
              onChange={handleChange}
            />
          </span>
        </div>
      )}
    </>
  );
};
