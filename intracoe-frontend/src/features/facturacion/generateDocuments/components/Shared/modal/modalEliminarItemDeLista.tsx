import { Dialog } from 'primereact/dialog';

interface ModalEliminarInterface {
  onClick?: (event: React.MouseEvent<HTMLButtonElement>) => void;
  visible: boolean;
  setVisible: any;
  size: number;
}

export const ModalEliminarItemDeLista: React.FC<ModalEliminarInterface> = ({
  onClick,
  visible,
  setVisible,
  size,
}) => {
  return (
    <div className="justify-content-center flex">
      <Dialog
        header="Eliminar de la lista"
        visible={visible}
        onHide={() => {
          if (!visible) return;
          setVisible(false);
        }}
      >
        <p className="m-0 py-5">
          ¿Seguro que quiere eliminar {size} productos de la factura?
        </p>
        <span className="flex justify-end gap-2">
          <button
            className="bg-red rounded-md px-4 py-2 text-white hover:cursor-pointer"
            onClick={onClick}
          >
            Eliminar
          </button>
          <button
            className="border-grauy text-grauy rounded-md border px-4 py-2 hover:cursor-pointer"
            onClick={() => setVisible(false)}
          >
            Cancelar
          </button>
        </span>
      </Dialog>
    </div>
  );
};
