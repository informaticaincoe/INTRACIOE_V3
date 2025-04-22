import React, { useState } from 'react';
import { IoEyeOutline } from 'react-icons/io5';
import { MdDeleteOutline } from 'react-icons/md';
import { RiEdit2Line } from 'react-icons/ri';
import { DeleteModal } from '../modales/deleteModal';
import { ViewModal } from '../modales/viewModal';
import { EditModal } from '../../../../../shared/modales/editModal';
import { ActivitiesData } from '../../../../../shared/interfaces/interfaces';

type ActionsProps = {
  activity: ActivitiesData;
  onDelete: () => void;
};

const Actions: React.FC<ActionsProps> = ({ activity, onDelete }) => {
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [showViewModal, setShowViewModal] = useState(false);
  const [showEditModal, setEditViewModal] = useState(false);

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

  const handleEdit = (activity: ActivitiesData) => {
    setSelectedActivity(activity);
    setEditViewModal(true);
  };

  return (
    <>
      <div className="group flex gap-5 text-sm">
        <button
          className="flex items-center gap-1 hover:cursor-pointer"
          onClick={() => handleview(activity)}
        >
          <IoEyeOutline
            size={20}
            style={{ color: 'var(--color-primary-yellow)' }}
          />
          <p className="text-primary-yellow">Ver</p>
        </button>
        <button
          className="flex items-center gap-1 hover:cursor-pointer"
          onClick={() => handleDelete(activity)}
        >
          <MdDeleteOutline size={20} style={{ color: 'var(--color-red)' }} />
          <p className="text-red">Eliminar</p>
        </button>
        <button
          className="flex items-center gap-1 hover:cursor-pointer"
          onClick={() => handleEdit(activity)}
        >
          <RiEdit2Line size={20} style={{ color: 'var(--color-blue)' }} />
          <p className="text-blue">Editar</p>
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
      {showEditModal && selectedActivity && (
        <EditModal
          activity={selectedActivity}
          visible={showEditModal}
          setVisible={setEditViewModal}
          onClose={() => setEditViewModal(false)}
          onDelete={onDelete}
        />
      )}
    </>
  );
};

export default Actions;
