import React, { createContext, useState, ReactNode } from 'react';
import { ActivitiesData } from '../interfaces/activitiesData';

interface ActivitiesContextType {
  activities: ActivitiesData[];
  setActivities: React.Dispatch<React.SetStateAction<ActivitiesData[]>>;
}

// Contexto puede ser ActivitiesContextType o null porque al principio no tiene valor
const ActivitiesContext = createContext<ActivitiesContextType | null>(null);

interface ActivitiesProviderProps {
  children: ReactNode;
}

export const ActivitiesProvider: React.FC<ActivitiesProviderProps> = ({
  children,
}) => {
  const [activities, setActivities] = useState<ActivitiesData[]>([]);

  return (
    <ActivitiesContext.Provider value={{ activities, setActivities }}>
      {children}
    </ActivitiesContext.Provider>
  );
};

export default ActivitiesContext;
