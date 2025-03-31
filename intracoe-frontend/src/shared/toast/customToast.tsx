// components/CustomToast.tsx
import React, { useRef, forwardRef, useImperativeHandle } from 'react';
import { Toast } from 'primereact/toast';
import { FaCircleCheck } from 'react-icons/fa6';

export type ToastSeverity =
  | 'success'
  | 'info'
  | 'warn'
  | 'error'
  | 'secondary'
  | 'contrast';

export type ToastOptions = {
  severity?: ToastSeverity;
  summary: string;
  detail?: string;
  icon?: React.ReactNode;
  sticky?: boolean;
  life?: number;
};

export type CustomToastRef = {
  show: (options: ToastOptions) => void;
};

const CustomToast = forwardRef<CustomToastRef>((props, ref) => {
  const toastRef = useRef<Toast>(null);

  useImperativeHandle(ref, () => ({
    show: ({
      severity = 'info',
      summary,
      detail,
      icon,
      sticky = true,
      life = 3000,
    }) => {
      toastRef.current?.clear();
      toastRef.current?.show({
        severity,
        summary,
        detail,
        sticky,
        life,
        content: (props) => (
          <div
            className="align-items-center flex gap-3 px-4 py-3"
            style={{ flex: 1 }}
          >
            {icon ?? <FaCircleCheck size={24} />}
            <div>
              <div className="text-900 text-lg font-bold">
                {props.message.summary}
              </div>
              {detail && <div className="text-700 text-sm">{detail}</div>}
            </div>
          </div>
        ),
      });
    },
  }));

  return <Toast ref={toastRef} position="bottom-center" />;
});

export default CustomToast;
