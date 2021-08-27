import React from "react";
import "./Image.css";

/** Renders the image */
function Image( {link}) {
    return (
        <div className="Image text-center">
            <img src={link} alt="" className="Image-img"></img>
        </div>
    )
}

export default Image;