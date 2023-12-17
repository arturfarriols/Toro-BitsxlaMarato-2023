import React, { useState, useEffect } from 'react';

const FileSelector = ({ onSelectFile }) => {
  const [fileList, setFileList] = useState([]);
  const [selectedFile, setSelectedFile] = useState(null);

  useEffect(() => {
    // Fetch file list from the backend when the component mounts
    fetch('http://localhost:8181/api/files')  // Update with your actual server URL
      .then(response => response.json())
      .then(data => setFileList(data.files))
      .catch(error => console.error('Error fetching file list:', error));
  }, []);

  const handleFileSelect = (file) => {
    // Pass the selected file to the parent component
    onSelectFile(file);
    setSelectedFile(file);
  };

  return (
    <div>
      <h2>File Selector:</h2>
      <ul>
        {fileList.map((file, index) => (
          <li key={index}>
            <label>
              <input
                type="radio"
                name="selectedFile"
                value={file}
                checked={selectedFile === file}
                onChange={() => handleFileSelect(file)}
              />
              {file}
            </label>
          </li>
        ))}
      </ul>
    </div>
  );
};

const AnalysisResult = ({ data }) => {
    // Assuming data is the JSON data you want to display
    const { contractions, mean, is_FCFB_determined, variability, amount_accelerations, amount_decelerations } = data;
  
    return (
      <div>
        <h2>Analysis Result:</h2>
        <ul>
          <li><strong>Contractions:</strong> {JSON.stringify(contractions)}</li>
          <li><strong>Mean:</strong> {mean}</li>
          <li><strong>Is FCFB Determined:</strong> {is_FCFB_determined ? 'True' : 'False'}</li>
          <li><strong>Variability:</strong> {variability}</li>
          <li><strong>Amount of Accelerations:</strong> {amount_accelerations}</li>
          <li><strong>Amount of Decelerations:</strong> {amount_decelerations}</li>
        </ul>
      </div>
    );
  };
  
const FileList = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [okResponse, setOkResponse] = useState(null)
  const handleFileSelect = (file) => {
    setSelectedFile(file);
  };

  const handleUpload = () => {
    if (selectedFile) {
      // Send selected file path to the backend
      fetch('http://localhost:8181/api/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ path: selectedFile }),
      })
        .then(response => response.json())
        .then(data => {
          console.log('Response from backend:', data);
          setOkResponse(data)
          // Handle the response as needed
        })
        .catch(error => {
          console.error('Error sending request to the backend:', error);
        });
    } else {
      console.error('No file selected.');
    }
  };
  return (
    <div>
      {okResponse ? (
        // Render content when okResponse is available
        <AnalysisResult data={okResponse} />
      ) : (
        // Render file selector when okResponse is not available
        <div>
          <FileSelector onSelectFile={handleFileSelect} />
          <div>
            <h2>Selected File:</h2>
            {selectedFile ? <p>{selectedFile}</p> : <p>No file selected</p>}
          </div>
          <button onClick={handleUpload}>Upload Selected File</button>
        </div>
      )}
    </div>
  );
};
  

export default FileList;