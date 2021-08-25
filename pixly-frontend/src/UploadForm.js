import React, { useState } from "react";

/** Image Upload Form 
 * 
 * props:
 * -upload
 * 
 * state:
 * - userFile
 * 
 * App -> UploadForm
*/

function UploadForm({ upload }) {
  const [userFile, setUserFile] = useState({ file: null});

  function handleChange(evt) {
    console.log("handleChange", evt.target.files)
    setUserFile({ file: evt.target.files[0]});
    console.log("USER FILE", userFile)
  }

  function handleSubmit(evt) {
    evt.preventDefault();
    upload(userFile);
    setUserFile({ file: null});
  }

  return (
    <form encType="multipart/form-data"
          onSubmit={handleSubmit}
          className="UploadForm container">
      <div className="form-group">
        <label htmlFor="userFile">Upload an image file</label>
        <input type="file" 
               name="user_file" 
               id="userFile"
               className="form-control"
               onChange={handleChange} />
        <button type="submit" className="btn btn-primary mt-3">Upload!</button>
      </div>
    </form>
  );
}
// end

export default UploadForm;