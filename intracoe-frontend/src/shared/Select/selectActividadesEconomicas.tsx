import { Dropdown } from 'primereact/dropdown';
import { useState } from 'react';
import './selectCustomStyle.css';

interface selectActividadesEconomicasInterface {
  actividades: any;
  setActividades: any;
}

export const SelectActividadesEconomicas: React.FC<
  selectActividadesEconomicasInterface
> = ({ actividades, setActividades }) => {
  const cities = [
    { name: 'Transporte de pasajeros marítimo y de cabotaje', code: '1' },
    { name: 'Venta al por menor de textiles y confecciones usados', code: '2' },
    {
      name: 'Venta al por menor de medicamentos farmacéuticos y otros materiales y artículos de uso médico, odontológico y veterinario',
      code: '3',
    },
    { name: 'Almacenes (venta de diversos artículos)', code: '4' },
    {
      name: 'Reparación y reconstrucción de vías, stop y otros artículos de fibra de vidrio',
      code: '5',
    },
    {
      name: 'Venta al por menor de materiales de construcción, electrodomésticos, accesorios para autos y similares en puestos de feria y mercados',
      code: '6',
    },
  ];

  return (
    <div className="justify-content-center flex">
      <Dropdown
        value={actividades}
        onChange={(e) => setActividades(e.value)}
        options={cities}
        optionLabel="name"
        placeholder="Seleccionar actividad economica"
        className="md:w-14rem font-display w-full"
        filter
      />
    </div>
  );
};
