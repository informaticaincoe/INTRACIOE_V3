// src/.../EditModal.tsx
import React, { useState, useEffect } from 'react';
import { Dialog } from 'primereact/dialog';
import { Input } from '../forms/input';
import { ActivitiesData } from '../interfaces/interfaces';

interface DeleteModalProps {
  items: any;
  visible: boolean;
  setVisible: (v: boolean) => void;
  onSave: () => void; // callback tras guardar para refrescar tabla y cerrar modal
  deleteFunction: (id: number) => Promise<any>;
}

export const EditModal: React.FC<DeleteModalProps> = ({
  items,
  visible,
  setVisible,
  onSave,
  deleteFunction,
}) => {
  const handlerForm = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      // Aquí uso la función dinámica que viene por props
      items.map(async (item: any) => {
        await deleteFunction(item.id);
      });
      onSave();
    } catch (err) {
      console.error(err);
      // mostrar toast de error si quieres
    }
  };

  return (
    <Dialog
      header="Eliminar registro"
      visible={visible}
      style={{ width: '60vw' }}
      onHide={() => setVisible(false)}
    >
      <form className="flex flex-col gap-7 px-5" onSubmit={handlerForm}>
        <label>eliminar</label>
        <div className="flex justify-end gap-3">
          <button
            type="submit"
            className="bg-primary-blue rounded px-6 py-2 text-white"
          >
            Guardar
          </button>
        </div>
      </form>
    </Dialog>
  );
};
