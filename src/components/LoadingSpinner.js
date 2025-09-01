import React from 'react';
import { Spinner } from '@nextui-org/react';

const LoadingSpinner = ({ text = "Loading..." }) => {
  return (
    <div className="flex items-center gap-3">
      <Spinner size="sm" color="current" />
      {text}
    </div>
  );
};

export default LoadingSpinner;
