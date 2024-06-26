import React, { useState } from 'react';
import ImageUpload from './components/ImageUpload';
import ResultDisplay from './components/ResultDisplay';

function App() {
  const [predictionResult, setPredictionResult] = useState(null);

  const handleResultReceived = (result) => {
    setPredictionResult(result);
  };

  return (
    <div className="container mx-auto p-8">
      <h1 className="text-4xl font-bold text-center mb-8">MNIST Digit Classifier</h1>
      <div className="max-w-md mx-auto bg-card text-card-foreground rounded-lg shadow-lg p-6">
        <ImageUpload onResultReceived={handleResultReceived} />
        <ResultDisplay result={predictionResult} />
      </div>
    </div>
  );
}

export default App;
