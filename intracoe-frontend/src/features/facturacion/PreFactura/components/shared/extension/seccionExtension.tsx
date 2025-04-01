import { Extension } from '../../../interfaces/facturaPdfInterfaces';

interface ExtensionInterfaceProps {
  extension: Extension;
}

export const SeccionExtension: React.FC<ExtensionInterfaceProps> = ({
  extension,
}) => {
  return (
    <div className="flex h-full flex-col gap-8">
      <div className="border-border-color grid h-full grid-rows-2 rounded-md border-2 px-4 py-3 text-start">
        <div className="grid grid-cols-[70%_30%] justify-between">
          <p>
            <span className="font-bold">
              Responsable por parte del emisor:{' '}
            </span>
            {extension.nombEntrega}
          </p>
          <p>
            <span className="font-bold">N° de documento: </span>
            {extension.nombEntrega}
          </p>
        </div>
        <div className="grid grid-cols-[70%_30%] justify-between">
          <p>
            <span className="font-bold">
              Responsable por parte del receptor
            </span>
            {extension.nombEntrega}
          </p>
          <p>
            <span className="font-bold">N° de documento: </span>
            {extension.nombEntrega}
          </p>
        </div>
      </div>
    </div>
  );
};
