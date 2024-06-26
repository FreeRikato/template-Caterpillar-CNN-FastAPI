import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";

const ResultDisplay = ({ result }) => {
  return (
    <Card className="mt-8">
      <CardHeader>
        <CardTitle>Prediction Result</CardTitle>
      </CardHeader>
      <CardContent>
        {result !== null ? (
          <p className="text-lg">The predicted digit is: <span className="font-semibold">{result}</span></p>
        ) : (
          <p className="text-lg">No prediction available yet. Please upload an image.</p>
        )}
      </CardContent>
    </Card>
  );
};

export default ResultDisplay;
