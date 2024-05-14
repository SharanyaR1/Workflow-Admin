import React, { useState } from 'react';
import { saveAs } from 'file-saver';
import './Upload.css';

function Modify() {
  const [tarball, setTarball] = useState({ preview: '', data: '' });
  const [jsonFile, setJsonFile] = useState({ preview: '', data: '' });
  const [status, setStatus] = useState('');
  const [dockerCredentials, setDockerCredentials] = useState({ id: '', password: '' });
  const [showDialog, setShowDialog] = useState(false);

  const uploadFiles = async () => {
    const formData = new FormData();
    
    // Append the tarball file
    if (tarball.data) {
      formData.append('tar', tarball.data);
    }
  
    // Append the JSON file
    if (jsonFile.data) {
      formData.append('file', jsonFile.data);
    }
  
    const options = {
      method: 'POST',
      body: formData
    };
  
    try {
      const response = await fetch('http://127.0.0.1:5000/upload', options);
      const data = await response.json();
      if (response.ok) {
        console.log('Files uploaded successfully');
      } else {
        console.error('Files upload failed:', data.message);
      }
    } catch (error) {
      console.error('Error uploading files:', error);
    }
  };
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    setShowDialog(true);
    await uploadFiles();
    // Clear form and status
    setTarball({ preview: '', data: '' });
    setJsonFile({ preview: '', data: '' });
    setStatus('');
    setShowDialog(false);
  };
  
  const handleTarballChange = (e) => {
    const file = e.target.files[0];
    const tarballFile = {
      preview: URL.createObjectURL(file),
      data: file,
    };
    setTarball(tarballFile);
  };
  
  const handleJsonFileChange = (e) => {
    const file = e.target.files[0];
    const jsonFileData = {
      preview: URL.createObjectURL(file),
      data: file,
    };
    setJsonFile(jsonFileData);
  };
  
  
  

  const handleDialogSubmit = async (e) => {
    e.preventDefault();
    // Process DockerHub credentials and file uploads here
    console.log('Submitting to DockerHub with ID:', dockerCredentials.id, 'and password:', dockerCredentials.password);
    // Clear form and status
    setTarball({ preview: '', data: '' });
    setJsonFile({ preview: '', data: '' });
    setStatus('');
    setShowDialog(false);
  };

  const handleChange = (e) => {
    setDockerCredentials({ ...dockerCredentials, [e.target.name]: e.target.value });
  };

  const handleCloseDialog = () => {
    setShowDialog(false);
  };

  const handledownloadButtonClick = async () => {
    try {
      const response = await fetch(`http://127.0.0.1:5000/download`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        }
      });
  
      if (!response.ok) {
        throw new Error('Failed to download file');
      }
  
      const blob = await response.blob();
      saveAs(blob, 'standard-format.json');
    } catch (error) {
      console.error('Error downloading file:', error);
    }
  };

  return (
    
    <div className='upload-container'>
      <h1>Upload to server</h1>
      <div className='upload'>
        
        <div className="upload-section">
          <h3>Upload Tarball</h3>
          {tarball.preview && <img src={tarball.preview} alt="Tarball Preview" width='100' height='100' />}
          <input type='file' name='tarballFile' onChange={handleTarballChange} />
        </div>
        <div className="upload-section">
          <h3>Upload JSON</h3>
          {jsonFile.preview && <img src={jsonFile.preview} alt="JSON Preview" width='100' height='100' />}
          <input type='file' name='jsonFile' onChange={handleJsonFileChange} />
        </div>
        <div className="upload-section">
          <button onClick={handledownloadButtonClick}>Download Sample File</button>
        </div>
      </div>
      <button className="submit-button" onClick={handleSubmit}>Submit</button>

      {showDialog && (
  <div className="dialog-overlay">
    <div className="dialog">
      <span className="close" onClick={handleCloseDialog}>&times;</span>
      <h2>Enter DockerHub Credentials</h2>
      <form onSubmit={handleDialogSubmit}>
        <label htmlFor="dockerId">DockerHub ID:</label>
        <input type="text" id="dockerId" name="id" value={dockerCredentials.id} onChange={handleChange} required />
        <label htmlFor="dockerPassword">DockerHub Password:</label>
        <input type="password" id="dockerPassword" name="password" value={dockerCredentials.password} onChange={handleChange} required />
        <div className="dialog-buttons">
          <button type="submit">Submit</button>
        </div>
      </form>
    </div>
  </div>
)}

    </div>
  );
}

 

export default Modify;