import React, { ReactNode, forwardRef } from 'react';
import { Stepper, StepperProps } from 'primereact/stepper';

interface CustomStepperProps extends StepperProps {
  children: ReactNode;
}

const CustomStepper = forwardRef<Stepper, CustomStepperProps>(({ children, ...rest }, ref) => {
  return (
    <>
      <Stepper ref={ref} {...rest} />
      {children}
    </>
  );
});


export default CustomStepper;
