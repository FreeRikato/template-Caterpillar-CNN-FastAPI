import React, { useState } from 'react';
import axios from 'axios';
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";


const ImageUpload = ({ onResultReceived }) => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    setSelectedFile(file);

    const reader = new FileReader();
    reader.onloadend = () => {
      setPreviewUrl(reader.result);
    };
    reader.readAsDataURL(file);
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      alert('Please select an image first!');
      return;
    }

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await axios.post('http://localhost:8000/predict', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      onResultReceived(response.data.prediction);
    } catch (error) {
      console.error('Error uploading image:', error);
      alert('Error uploading image. Please try again.');
    }
  };

  return (
    <div className="flex flex-col items-center mt-4">
      <Input 
        type="file" 
        onChange={handleFileChange} 
        accept="image/*" 
        className="mb-4"
      />
      {previewUrl && <img src={previewUrl} alt="Preview" className="max-w-xs mb-4 rounded-md" />}
      <Button onClick={handleUpload} className="w-full">
        Upload and Predict
      </Button>
    </div>
  );
};

export default ImageUpload;
