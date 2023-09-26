import {BrowserRouter as Router, Route, Switch} from "react-router-dom";

import Register from "./components/registration/Register/Register";
import Login from "./components/registration/Login/Login";
import Verification from "./components/registration/Verification/Verification";
import RecoveryPassEmail from "./components/registration/RecoveryPassEmail/RecoveryPassEmail";
import RecoveryPass from "./components/registration/RecoveryPass/RecoveryPass";
import Home from "./components/Home/Home";
import FormEditProfile from "./components/FormEditProfile/FormEditProfile";
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
                     <Route path="/account/edit">
                        <FormEditProfile/>
                    </Route>
                    <Route path="/account/im">
                        <Home/>
                    </Route>
                    <Route path="/">
                        <Login/>
                    </Route>
                </Switch>
            </div>
        </Router>
  )
}

export default App;
