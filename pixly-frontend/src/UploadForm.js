import React, { useState } from "react";

/** Image Upload Form */

function UploadForm({ upload }) {
  const [userFile, setUserFile] = useState("");

  function handleChange(evt) {
    setUserFile(evt.target.value);
  }

  function handleSubmit(evt) {
    evt.preventDefault();
    upload(userFile);
    setUserFile("");
  }

  return (
    <form encType="multipart/form-data" onSubmit={handleSubmit}>
      <label htmlFor="userFile">Upload an image file</label>
      <input type="file" name="userFile" value={userFile} onChange={handleChange} />
      <button>Upload!</button>
    </form>
  );
}
// end

export default UploadForm;