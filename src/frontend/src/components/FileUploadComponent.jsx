import React, { useState } from 'react';
import { handleUpload } from '../functions/handleFileUpload';
import { formatSize } from '../functions/formatSize';

const FileUploadComponent = () => {
    const [file, setFile] = useState(null);
    const [errorMessage, setErrorMessage] = useState('');
    const [uploadClicked, setUploadClicked] = useState(false);
    const [result, setResult] = useState(null);


    const handleFileChange = (event) => {
        console.log(import.meta.env.BACKEND_SVC) // 123

        setFile(event.target.files[0]);
    };



    /* const handleFileUpload = () => {
         if (!file) {
             //setErrorMessage('Please select a file');
             setUploadClicked(true);
             return;
         }
 
         handleUpload(file)
             .then((response) => {
                 console.log('File uploaded successfully:', response);
                 setErrorMessage('');
                 setUploadClicked(false);
                 setResult(response); 
             })
             .catch((error) => {
                 console.error('Error uploading file:', error.message);
             });
     };*/
     const handleFileUpload = async (file) => {
        try {
          const formData = new FormData();
          formData.append('file', file);
      
          const response = await fetch('http://localhost:8181/upload', {
            method: 'POST',
            body: formData,
            headers:   {
              
              //  "Content-Type": "multipart/form-data",
                 'Content-Type': 'application/x-www-form-urlencoded',
              },
          });
          if (!response.ok) {
            throw new Error('Network response was not ok.');
          }
      
          const disposition = response.headers.get('Content-Disposition');
          const fileNameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
          const [, filename] = fileNameRegex.exec(disposition) || [];
          
          const blob = await response.blob();
          const downloadUrl = URL.createObjectURL(blob);
      
          const downloadButton = document.getElementById('downloadButton');
          downloadButton.href = downloadUrl;
          downloadButton.download = filename || 'files.zip';
          downloadButton.click();
      
          // Cleanup
          setTimeout(() => {
            URL.revokeObjectURL(downloadUrl);
            downloadButton.href = '#';
          }, 100); // Delay to allow download and clean-up
        } catch (error) {
          console.error('Error uploading file:', error);
          // Handle errors such as network issues, server errors, etc.
          // Show an error message to the user
        }
      };
    const handleFileUpload3 = async (file) => {
        try {
            const formData = new FormData();
            formData.append('file', file);

            const response = await fetch('http://localhost:8181/upload', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                throw new Error('Network response was not ok.');
            }

            const metadataValue = response.headers.get('Custom-Metadata'); // Get custom metadata from header

            const blob = await response.blob(); // Get response as blob
            const downloadUrl = URL.createObjectURL(blob); // Create object URL for the blob

            // Create a download button and trigger download on button click
            const downloadButton = document.createElement('a');
            downloadButton.href = downloadUrl;

                        
            // Get the current date and time
            const currentDateTime = new Date().toISOString().replace(/[-T:]/g, '').split('.')[0]; // Format: YYYYMMDDHHMMSS

            // Set the filename using the current date and time
            const fileName = `files_${currentDateTime}.zip`;

            downloadButton.download = fileName; // Set the filename for download
            downloadButton.textContent = 'Download ZIP';
            document.body.appendChild(downloadButton);

            downloadButton.click(); // Trigger click to initiate download

            // Cleanup: Remove the download button and revoke object URL
            //downloadButton.remove();
            //URL.revokeObjectURL(downloadUrl);
        } catch (error) {
            console.error('Error uploading file:', error);

        }
    };

    document.addEventListener('change', (event) => {
        if (event.target && event.target.id === 'file_input') {
            const file = event.target.files[0];
            if (file) {
                handleFileUpload(file);
            } else {
                console.error('No file selected.');
                // Handle no file selected scenario
            }
        }
    });
    const renderResult = () => {
        if (result) {
            return (
                <div>
                    <pre>{JSON.stringify(result, null, 2)}</pre>
                    <p>Uploaded File: {file.name}</p>
                </div>
            );
        }
        return null;
    };


    return (

        <div className="py-10">
            <div className="max-w-md mx-auto p-4 py-6 bg-white rounded-lg shadow-md pb-10">
                <label htmlFor="file_input" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">

                </label>
                <input
                    id="file_input"
                    type="file"
                    onChange={handleFileChange}
                    className="block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400"
                    aria-describedby="file_input_help"
                />
                <p className="mt-1 text-sm text-gray-500 dark:text-gray-300" id="file_input_help">
                    {file ? `Selected file: ${file.name}` : 'PDF, ZIP, ...'}
                </p>
                <p className="mt-1 text-sm text-gray-500 dark:text-gray-300" id="file_input_help">
                    {file ? `Size: ${formatSize(file.size)} (${(file.size / (1024 * 1024)).toFixed(2)} MB)` : ' '}
                </p>
                {errorMessage && <div className="text-red-500 mt-2">{errorMessage}</div>}

                <button
                    onClick={handleFileUpload}
                    className=" mt-4   flex flex-col items-center rounded-full border-2 inline-block border-primary focus:outline-none  px-6 pb-[6px] pt-2 text-xs font-medium uppercase leading-normal text-primary transition duration-150 ease-in-out hover:border-primary-600 hover:bg-neutral-500 hover:bg-opacity-10 hover:text-primary-600 focus:border-primary-600 focus:text-primary-600 focus:outline-none focus:ring-0 active:border-primary-700 active:text-primary-700 dark:hover:bg-neutral-100 dark:hover:bg-opacity-10"
                    data-te-ripple-init>
                    Upload
                </button>
                {uploadClicked && !file && <p className="text-red-500 mt-2">Please select a file to upload.</p>}
            </div>
            <button id="downloadButton">Download</button>

            <div className="mt-4">
                {renderResult()} {/* Display the result here */}

            </div>

        </div>


    );
};

export default FileUploadComponent;