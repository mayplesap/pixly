import React, { useState } from "react";

/** Image Upload Form 
 * 
 * props:
 * -upload
 * 
 * state:
 * - formData
 * 
 * App -> UploadForm
*/

function UploadForm({ upload }) {
  const [formData, setFormData] = useState({ file: null }); // rename to something like formData, so if also had a title and a desc, we could data.append each one, or iterate over and dynamically add them

  function handleChangeFile(evt) {
    setFormData({ ...formData, file: evt.target.files[0]});
  }
  function handleChange(evt) {
    const { name, value } = evt.target
    setFormData(data => ({
      ...formData,
      [name]: value
    }));
  }

  function handleSubmit(evt) {
    evt.preventDefault();
    const data = new FormData(); // have to append indiv key/value pairs once we have more form fields (see line 15)
    console.log("FORMDATA", formData);
    for(let key in formData) {
      data.append(key, formData[key]);
    }
  //   for(let pair of data.entries()) {
  //     console.log(pair[0]+ ', '+ pair[1]);
  //  }
    // data.append("name", formData.file);
    upload(data);
    setFormData({ file: null });
  }

  return (
    <form encType="multipart/form-data"
          action=""
          onSubmit={handleSubmit}
          className="UploadForm container">
      <div className="form-group">
        <label htmlFor="name">Name of Image</label>
        <input name="name"
               id="name"
               onChange={handleChange}
               className="form-control"/>
        <label htmlFor="category">Category</label>
        <input name="category"
               id="category"
               onChange={handleChange}
               className="form-control"/>
        <label htmlFor="uploadedBy">Uploaded By</label>
        <input name="uploadedBy"
               id="uploadedBy"
               onChange={handleChange}
               className="form-control"/>
               
        <label htmlFor="file">Upload an image file</label>
        <input type="file" 
               name="file" 
               id="file"
               className="form-control"
               onChange={handleChangeFile} />
        <button type="submit" className="btn btn-primary mt-3">Upload!</button>
      </div>
    </form>
  );
}
// end

export default UploadForm;