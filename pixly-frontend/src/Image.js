import React from "react";
import "./Image.css";

function Image( {link}) {
    return (
        <div className="Image text-center">
            <img src={link} alt="" className="Image-img"></img>
        </div>
    )
}

export default Image;