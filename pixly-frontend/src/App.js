import React, { useState, useEffect } from "react";
import UploadForm from "./UploadForm";
import PixlyApi from "./api";
import "bootstrap/dist/css/bootstrap.css"
import './App.css';
import Image from "./Image";

function App() {
 
    const [link, setLink] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [border, setBorder] = useState(null);
  
    async function upload(data) {
      console.log("APP UPLOAD", data);
      const response = await PixlyApi.uploadImage(data);
      const imgLink = response.data;
      setLink(imgLink);
      const bi = await PixlyApi.borderImage();
      console.log("BI", bi)
      setBorder(bi);
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
          <Image link={border} />
          <UploadForm upload={upload} />
        </div>
  );
}

export default App;
