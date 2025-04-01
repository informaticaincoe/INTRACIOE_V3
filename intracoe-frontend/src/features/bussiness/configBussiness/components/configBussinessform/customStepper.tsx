import React, { ReactNode, forwardRef } from 'react';
import { Stepper, StepperProps } from 'primereact/stepper';

interface CustomStepperProps extends StepperProps {
  children: ReactNode;
}

const CustomStepper = forwardRef<Stepper, CustomStepperProps>((props, ref) => {
  return <Stepper ref={ref} {...props}>{props.children}</Stepper>;
});

export default CustomStepper;
