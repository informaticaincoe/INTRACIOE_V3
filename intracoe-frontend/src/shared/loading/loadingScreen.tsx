import { FaSpinner } from 'react-icons/fa';

const LoadingScreen = () => {
  return (
    <div className="fixed inset-0 z-[100] flex items-center justify-center bg-black opacity-50">
      <FaSpinner className="animate-spin text-6xl text-white" />
    </div>
  );
};

export default LoadingScreen;
