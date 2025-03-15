import { useEffect, useRef, useState } from 'react';
import { ActivitiesData } from '../../features/facturacion/activities/interfaces/activitiesData';
import { Toast } from 'primereact/toast';
import { ConfirmDialog, confirmDialog } from 'primereact/confirmdialog';
import { Dialog } from 'primereact/dialog';
// import styles from "./modalCustom.module.css"

interface ViewModalProps {
  activity: ActivitiesData;
  visible: boolean;
  setVisible: any;

}

export const ViewModal: React.FC<ViewModalProps> = ({ activity, visible, setVisible }) => {

  return (
    <>
      <Dialog header={<p className="text-2xl px-10">Detalle actividad económica</p>} visible={visible} style={{ width: '50vw' }} onHide={() => { if (!visible) return; setVisible(false); }}>
        <div className="flex-column align-items-center border-bottom-1 surface-border flex w-full px-7">
          <table className="font-display text-md">
            <tbody>
              <tr>
                <td className="text-gray px-5 py-2">Codigo:</td>
                <td className="text-black">{activity.codigo}</td>
              </tr>
              <tr>
                <td className="text-gray px-5">Descripción:</td>
                <td className="text-black">{activity.descripcion}</td>
              </tr>
            </tbody>
          </table>

        </div>
        <div className='flex justify-end'>
          <button className='bg-primary-blue text-white rounded-md px-7 py-2 flex justify-end border hover:cursor-pointer' onClick={()=>setVisible(false) }>
            Ok
          </button>
        </div>
      </Dialog>
    </>
  );
};
