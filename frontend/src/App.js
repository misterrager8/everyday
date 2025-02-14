import "bootstrap/dist/css/bootstrap.css";
import "bootstrap/dist/js/bootstrap.js";
import "bootstrap-icons/font/bootstrap-icons.css";

import "./App.css";
import Display from "./components/organisms/Display";

function App() {
  return (
    <div className="row p-4" style={{ height: "100vh", width: "100vw" }}>
      <Display />
    </div>
  );
}

export default App;
