const  handleUpload = (file) => {
    if (!file) {
        console.error('No file selected');
        return;
    }

    const formData = new FormData();
    formData.append('file', file);
    
    fetch('http://localhost:8181/upload', {
        method: 'POST',
        body: formData,
    })
        .then((response) => {
            console.log(response);
            
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            console.log('File uploaded successfully');
        })
        .catch((error) => console.error('There was a problem with file upload:', error.message));
};

export { handleUpload };