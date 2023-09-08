import {Route,BrowserRouter as Router, Switch} from "react-router-dom";

import Register from "./components/Register/Register";
import Login from "./components/Login/Login";
import Verification from "./components/Verification/Verification";
import RecoveryPassEmail from "./components/RecoveryPassEmail/RecoveryPassEmail";
import RecoveryPass from "./components/RecoveryPass/RecoveryPass";
function App() {

    return (
        <Router>
            <div className="App">
                <Switch>
                    <Route path="/register">
                        <Register/>
                    </Route>
                    <Route exact path="/api/v1/login/activate/:uidb64/:token">
                        <Verification/>
                    </Route>
                    <Route exact path="/api/v1/login/reset_password/:uidb64/:token">
                        <RecoveryPass/>
                    </Route>
                    <Route path="/login/reset_password">
                        <RecoveryPassEmail/>
                    </Route>
                    <Route path="/">
                        <Login/>
                    </Route>
                </Switch>
            </div>
        </Router>
  );
}

export default App;
