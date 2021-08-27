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
    const [filterLink, setFilterLink] = useState(null);
  
    /** Functions to upload data, return an image link, and setsstate */
    async function upload(data) {
      const response = await PixlyApi.uploadImage(data);
      const imgLink = response.data;
      setLink(imgLink);
    }

    async function blackWhiteImage() {
      setIsLoading(true);
      const response = await PixlyApi.blackWhiteImage(link);
      setIsLoading(false);
      setFilterLink(response.data)
    }
    
    async function sepiaImage() {
      setIsLoading(true);
      const response = await PixlyApi.sepiaImage(link);
      setIsLoading(false);
      setFilterLink(response.data)
    }
    
    async function colorMergeImage() {
      setIsLoading(true);
      const response = await PixlyApi.colorMergeImage(link);
      setIsLoading(false);
      setFilterLink(response.data)
    }

    async function pointilizeImage() {
      setIsLoading(true);
      const response = await PixlyApi.pointilizeImage(link);
      setIsLoading(false);
      setFilterLink(response.data)
    }

    async function addBorder() {
      setIsLoading(true);
      const response = await PixlyApi.addBorder(link);
      setIsLoading(false);
      setFilterLink(response.data)
    }
  
    if (isLoading) return <i>Loading...</i>
  
    return (
        <div>
          {filterLink
          ?
          <Image link={filterLink} />
          :
          <Image link={link} />
          }

          <UploadForm upload={upload} />
          {link
          ?
          <ImageEditForm blackWhiteImage={blackWhiteImage} 
                         sepiaImage={sepiaImage} 
                         colorMergeImage={colorMergeImage} 
                         pointilizeImage={pointilizeImage}
                         addBorder={addBorder}
                         />
          : null
          }
        </div>
  );
}

export default App;
