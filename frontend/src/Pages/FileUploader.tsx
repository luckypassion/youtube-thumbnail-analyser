import { useState } from 'react';
import { Button } from "@/components/ui/button";
import axios from 'axios';

const FileUploader = () => {
    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const [res, setRes] = useState<string | null>(null);
    const [error, setError] = useState<string | null>(null);

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setRes(null);
        if (e.target.files && e.target.files.length > 0) {
            setError(null);
            setSelectedFile(e.target.files[0]);
        }
    };

    const handleUpload = async () => {
        if (selectedFile) {
            try {
                const formData = new FormData();
                formData.append('file', selectedFile);

                const response = await axios.post('http://localhost:8000/upload_thumbnail/', formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data',
                    },
                });

                setRes(JSON.stringify(response.data));
                console.log('File uploaded successfully:', response.data);
            } catch (error) {
                console.error('Error uploading file:', error);
                setRes('Error uploading file');
            }
        } else {
            console.log('No file selected');
            setError('No file selected');
        }
    };

    return (
        <div className='w-full'>
            <div className="max-w-[1100px] flex justify-center items-center h-auto">
                <div className="flex flex-col items-center space-y-4 p-6 bg-gray-300 shadow-lg rounded-xl w-full max-w-md">
                    <div className="container" style={{ cursor: 'pointer' }}>
                        <div className="folder">
                            <div className="front-side">
                                <div className="tip"></div>
                                <div className="cover"></div>
                            </div>
                            <div className="back-side cover"></div>
                        </div>
                        <label className="custom-file-upload">
                            <input
                                className="title hidden"
                                type="file"
                                accept="image/*"
                                onChange={handleFileChange}
                            />
                            <span className="text-white font-bold text-lg font-rubik">Choose a Thumbnail</span>
                        </label>
                    </div>

                    <div className="text-white font-bold text-lg font-oswald">
                        {selectedFile ? `File Name: ${selectedFile.name}` : 'Select a file to upload'}
                    </div>

                    <Button onClick={handleUpload} className="font-oswald" style={{ width: '100%', backgroundColor: '#3f51b5', color: 'white' }}>
                        Submit
                    </Button>

                    {res && (
                        <div className="mt-6 p-6 bg-white rounded-lg shadow-md w-full text-left space-y-2 font-rubik">
                            <h3 className="text-lg font-bold text-gray-700 font-oswald">Server Response</h3>
                            <p className="text-blue-600 font-semibold"><span className='font-oswald'>Score:</span> {JSON.parse(res).score}/10</p>
                            <p className="text-gray-600">{JSON.parse(res).comment}</p>
                        </div>
                    )}
                {error && <p className='text-red-500'>{error}</p>}

                </div>
            </div>
        </div>

    );
};

export default FileUploader;
