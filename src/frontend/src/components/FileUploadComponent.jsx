import React, { useState } from 'react';
import { handleUpload } from '../functions/handleFileUpload';
import {formatSize} from '../functions/formatSize';

const FileUploadComponent = () => {
    const [file, setFile] = useState(null);
    const [errorMessage, setErrorMessage] = useState('');
    const [uploadClicked, setUploadClicked] = useState(false);


    const handleFileChange = (event) => {
        console.log(import.meta.env.BACKEND_SVC) // 123

        setFile(event.target.files[0]);
    };



    const handleFileUpload = () => {
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

            })
            .catch((error) => {
                console.error('Error uploading file:', error.message);
            });
    };

    // Function to display file information in a div
    const renderFileInfo = () => {
        if (!file) {
            return <div>No file selected</div>;
        }

        return (
            <div>
                <p>File Name: {file.name}</p>
                <p>File Size: {file.size} bytes</p>
                <p>File Type: {file.type}</p>
            </div>
        );
    };



    return (

        <div>
            <div className="max-w-md mx-auto py-6 bg-white rounded-lg shadow-md pb-10">
                <label htmlFor="file_input" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">
                    Upload file
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
                    class="inline-block mt-4   flex flex-col items-center rounded-full border-2 inline-block border-primary focus:outline-none  px-6 pb-[6px] pt-2 text-xs font-medium uppercase leading-normal text-primary transition duration-150 ease-in-out hover:border-primary-600 hover:bg-neutral-500 hover:bg-opacity-10 hover:text-primary-600 focus:border-primary-600 focus:text-primary-600 focus:outline-none focus:ring-0 active:border-primary-700 active:text-primary-700 dark:hover:bg-neutral-100 dark:hover:bg-opacity-10"
                    data-te-ripple-init>
                    Upload
                </button>
                {uploadClicked && !file && <p className="text-red-500 mt-2">Please select a file to upload.</p>}

            </div>
        </div>


    );
};

export default FileUploadComponent;