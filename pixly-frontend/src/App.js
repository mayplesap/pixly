import React, { useState, useEffect } from "react";
import UploadForm from "./UploadForm";
import ImageEditForm from "./ImageEditForm";
import PixlyApi from "./api";
import "bootstrap/dist/css/bootstrap.css"
import './App.css';
import Image from "./Image";

function App() {
 
    const [link, setLink] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [bwLink, setBwLink] = useState(null);
  
    async function upload(data) {
      console.log("APP UPLOAD", data);
      const response = await PixlyApi.uploadImage(data);
      const imgLink = response.data;
      setLink(imgLink);
      // const bi = await PixlyApi.borderImage();
      // console.log("BI", bi)
      // setBorder(bi);
    }

    async function blackWhiteImage() {
      console.log("INSI BLACKWHITE IMAGE FUNCTION", link);
      const response = await PixlyApi.blackWhiteImage(link);
      console.log("BW IMAGE RESPONSE", response.data)
      setBwLink(response.data)
      console.log("BWLINK", bwLink)
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
          {bwLink
          ?
          <Image link={bwLink} />
          : null
          }
          <UploadForm upload={upload} />
          {link
          ?
          <ImageEditForm blackWhiteImage={blackWhiteImage}/>
          : null
          }
        </div>
  );
}

export default App;
