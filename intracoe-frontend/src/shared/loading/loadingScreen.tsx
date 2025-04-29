import { FaSpinner } from 'react-icons/fa';

interface LoadingScreenProps {
  text?: string;
}

const LoadingScreen: React.FC<LoadingScreenProps> = ({ text }) => {
  return (
    <div className="fixed inset-0 z-[100] flex flex-col items-center justify-center bg-[rgba(0,0,0,0.5)]">
      <FaSpinner className="animate-spin text-6xl text-white" />
      <p className="text-center text-3xl font-semibold text-white">{text}</p>
    </div>
  );
};

export default LoadingScreen;
