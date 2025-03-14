import React, { useState } from 'react';
import { IoEyeOutline } from 'react-icons/io5';
import { MdDeleteOutline } from 'react-icons/md';
import { ActivitiesData } from '../../interfaces/activitiesData';
import { DeleteModal } from '../../../../../shared/modal/deleteModal';
import { ViewModal } from '../../../../../shared/modal/viewModal';

type ActionsProps = {
  activity: ActivitiesData;
  onDelete: () => void;
};

const Actions: React.FC<ActionsProps> = ({ activity, onDelete }) => {
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [showViewModal, setShowViewModal] = useState(false);

  const [selectedActivity, setSelectedActivity] =
    useState<ActivitiesData | null>(null);

  const handleDelete = (activity: ActivitiesData) => {
    setSelectedActivity(activity);
    setShowDeleteModal(true);
  };

  const handleview = (activity: ActivitiesData) => {
    setSelectedActivity(activity);
    setShowViewModal(true);
  };

  return (
    <>
      <div className="group flex gap-5 text-sm">
        <button
          className="flex items-center gap-1 hover:cursor-pointer"
          onClick={() => handleview(activity)}
        >
          <IoEyeOutline size={20} color="#7C7C7C" />
          <p className="text-gray">Ver</p>
        </button>
        <button
          className="flex items-center gap-1 hover:cursor-pointer"
          onClick={() => handleDelete(activity)}
        >
          <MdDeleteOutline size={20} color="#FC0005" />
          <p className="text-red">Eliminar</p>
        </button>
      </div>

      {showDeleteModal && selectedActivity && (
        <DeleteModal
          activity={selectedActivity}
          onClose={() => setShowDeleteModal(false)}
          onDelete={onDelete}
        />
      )}

      {showViewModal && selectedActivity && (
        <ViewModal
          activity={selectedActivity}
          visible={showViewModal}
          setVisible={setShowViewModal}
        />
      )}
    </>
  );
};

export default Actions;
