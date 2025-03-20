import React from 'react';
import { Empresa } from '../../interfaces/empresaInterfaces';

type ActionsProps = {
  empresa: Empresa;
};

export const ActionsEmpresa: React.FC<ActionsProps> = ({ empresa }) => {
  return <div>Actions</div>;
};
