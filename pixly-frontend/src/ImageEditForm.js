import React, { useState } from "react";

/** Image Edit Form 
 * 
 * props:
 * -functions to filter image appearance
 * 
 * state:
 * - formData
 * 
 * App -> UploadForm
*/

function ImageEditForm({ blackWhiteImage, sepiaImage, colorMergeImage, pointilizeImage, addBorder}) {
  const [formData, setFormData] = useState({ filter: "blackWhiteImage" });  

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
    } else if (formData.filter === "pointilize") {
      pointilizeImage()
    } else if (formData.filter === "addBorder") {
      addBorder()
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
            <option value="pointilize">Pointilize</option>
            <option value="addBorder">Add Border</option>
        </select>
        <button type="submit" className="btn btn-primary mt-3">Apply Filter</button>
      </div>
    </form>
  );
}
// end

export default ImageEditForm;