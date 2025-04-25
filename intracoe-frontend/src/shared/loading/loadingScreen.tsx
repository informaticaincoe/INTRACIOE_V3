import { FaSpinner } from 'react-icons/fa';

const LoadingScreen = () => {
  return (
    <div className="fixed inset-0 bg-black opacity-50 flex justify-center items-center z-[100]">
      <FaSpinner className="text-white text-6xl animate-spin" />
    </div>
  );
};

export default LoadingScreen;
