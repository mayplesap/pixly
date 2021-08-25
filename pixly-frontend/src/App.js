import React, { useState, useEffect } from "react";
import UploadForm from "./UploadForm";
import PixlyApi from "./api";
import "bootstrap/dist/css/bootstrap.css"
import './App.css';

function App() {
 
    const [filename, setFilename] = useState("");
    const [link, setLink] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
  
    async function upload(filename) {
      setFilename(filename);
      console.log("APP UPLOAD", filename);
      let link = await PixlyApi.uploadImage(filename);
      console.log("LINK", link)
      setLink(link);
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
          <UploadForm upload={upload} />
        </div>
  );
}

export default App;
