import Sidebar from './Components/Sidebar/Sidebar'
import axios from "axios";


axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.withCredentials = true;

function App() {

  return (
    <div className="App">
     <Sidebar/>
    </div>
  );
}

export default App;
