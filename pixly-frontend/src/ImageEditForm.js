import React, { useState } from "react";

/** Image Edit Form 
 * 
 * props:
 * -
 * 
 * state:
 * - formData
 * 
 * App -> UploadForm
*/

function ImageEditForm({ blackWhiteImage, sepiaImage, colorMergeImage }) {
  const [formData, setFormData] = useState({ filter: "blackWhiteImage" }); // rename to something like formData, so if also had a title and a desc, we could data.append each one, or iterate over and dynamically add them

  function handleFilter(evt) {
    const { name, value } = evt.target;
    setFormData(data => ({
      [name]: value
    }))
  }

  function handleSubmit(evt) {
    evt.preventDefault();
    if(formData.filter === "blackWhiteImage") {
      blackWhiteImage()
    } else if (formData.filter === "sepiaImage") {
      sepiaImage()
    } else if (formData.filter === "colorMerge") {
      colorMergeImage()
    }
  }

  return (
    <form onSubmit={handleSubmit}
          className="ImageEditForm container">
      <div className="form-group">
        <label htmlFor="filters">Image Filter:&nbsp;&nbsp;</label>
        <select
          id="filter"
          name="filter"
          value={formData.filter}
          onChange={handleFilter}
          className="form-control">
            <option value="blackWhiteImage">Black &amp; White</option>
            <option value="sepiaImage">Sepia</option>
            <option value="colorMerge">Color Merge (Alien)</option>
        </select>
        <button type="submit" className="btn btn-primary mt-3">Apply Filter</button>
      </div>
    </form>
  );
}
// end

export default ImageEditForm;