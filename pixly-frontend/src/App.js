import React, { useState, useEffect } from "react";
import UploadForm from "./UploadForm";
import PixlyApi from "./api";
import "bootstrap/dist/css/bootstrap.css"
import './App.css';
import Image from "./Image";

function App() {
 
    // const [filename, setFilename] = useState("");
    const [link, setLink] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
  
    async function upload(filename) {
      // setFilename(filename);
      console.log("APP UPLOAD", filename);
      const response = await PixlyApi.uploadImage(filename);
      const imgLink = response.data;
      setLink(imgLink);
    }
  
    // useEffect(function uploadImage() {
    //   async function uploadImageGetLink() {
    //     const response = await axios.post(`${BASE_URL}`);
    //     setLink(response);
    //     setIsLoading(false);
    //   }
    //    uploadImageGetLink();
    // }, [filename]);
  
    if (isLoading) return <i>Loading...</i>
  
    return (
        <div>
          <Image link={link} />
          <UploadForm upload={upload} />
        </div>
  );
}

export default App;
