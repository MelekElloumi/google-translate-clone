import Translate from "./components/Translate";
import React from "react";
import Header from "./components/Header";


const App = () => {
  return (
    <div className="App">
      <Header />
      <div className="row" style={{ position: "relative" }}>
        <div className="row" style={{ border: "2px solid #e5e5e5", position: "absolute", background: "#fafafa", height: "110px", width: "110vw" }}>
          <div className="col-11 mx-auto">
          </div>
        </div>
        <div className="col-lg-11 mx-auto col-sm-12 p-0">
          <div style={{ height: "80px" }}></div>
          <Translate />
        </div>
      </div>
    </div>
  );
}

export default App;
