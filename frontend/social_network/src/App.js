import axios from "axios";
import Sidebar from './Components/Sidebar/Sidebar'

axios.get('api/v1/login/')
     .then(data => { console.log(data) })


function App() {

  return (
    <div className="App">
     <Sidebar/>
    </div>
  );
}

export default App;
