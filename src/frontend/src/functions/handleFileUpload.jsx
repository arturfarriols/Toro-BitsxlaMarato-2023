const handleUpload = (file) => {
    if (!file) {
        console.error('No file selected');
        return;
    }

    const formData = new FormData();
    formData.append('file', file);
    
    fetch(import.meta.env.VITE_BACKEND_SVC, {
        method: 'POST',
        body: formData,
    })
        .then((response) => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            console.log('File uploaded successfully');
        })
        .catch((error) => console.error('There was a problem with file upload:', error.message));
};

export { handleUpload };