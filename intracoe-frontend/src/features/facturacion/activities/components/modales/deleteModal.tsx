// src/.../DeleteModal.tsx
import React, { useEffect, useRef } from 'react';
import { ConfirmDialog, confirmDialog } from 'primereact/confirmdialog';
import { Toast } from 'primereact/toast';

interface DeleteModalProps<T extends { id: any; [key: string]: any }> {
  item: T | null;
  visible: boolean;
  setVisible: (v: boolean) => void;
  deleteFunction: (id: T['id']) => Promise<any>;
  onDeleted: () => void;
}

export function DeleteModal<T extends { id: any; [key: string]: any }>({
  item,
  visible,
  setVisible,
  deleteFunction,
  onDeleted,
}: DeleteModalProps<T>) {
  const toast = useRef<Toast>(null);

  // Mostrar el confirmDialog cuando se abra y haya un item
  useEffect(() => {
    if (visible && item) {
      confirmDialog({
        message: (
          <div className="flex flex-col">
            <span>¿Estás seguro de eliminar:</span>
            <strong className="mt-2 italic">
              {String(item.nombre ?? item.descripcion ?? item.id)}
            </strong>
          </div>
        ),
        header: 'Confirmar eliminación',
        icon: 'pi pi-exclamation-triangle',
        acceptLabel: 'Eliminar',
        rejectLabel: 'Cancelar',
        acceptClassName: 'p-button-danger',
        rejectClassName: 'p-button-text',
        accept: async () => {
          try {
            await deleteFunction(item.id);
            toast.current?.show({
              severity: 'success',
              summary: 'Eliminado',
              detail: 'El elemento fue eliminado correctamente',
              life: 3000,
            });
            onDeleted();
          } catch (err) {
            console.error(err);
            toast.current?.show({
              severity: 'error',
              summary: 'Error',
              detail: 'No se pudo eliminar',
              life: 3000,
            });
          } finally {
            setVisible(false);
          }
        },
        reject: () => {
          setVisible(false);
        },
      });
    }
  }, [visible, item, deleteFunction, onDeleted, setVisible]);

  return (
    <>
      <Toast ref={toast} />
      <ConfirmDialog />
    </>
  );
}
