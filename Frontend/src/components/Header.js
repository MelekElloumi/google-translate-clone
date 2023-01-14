import React, { useState } from "react";
import SideBar from "./SideBar";
import AuthGoogle from "../api/AuthGoogle";

const Header=()=>{
    const [isClicked, setIsClicked]=useState(false);
    const handleProfile=()=>{
        setIsClicked(!isClicked);
    }
    return(
        <div>
        <nav className="navbar navbar-light p-3">

          <div className="row" style={{ marginLeft: 30 }} >
            <a href="/" className="navbar-brand my-auto"><h3 className="text-secondary"><img alt="Google" height={25} src="google-logo.png"></img>  Translate</h3></a>
          </div>
        </nav>
      </div>
    );
}

export default Header;