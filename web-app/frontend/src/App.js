import { useState } from 'react';
import styles from './App.module.scss'
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import './App.scss';
import i18n from './i18n';
import { I18nextProvider } from 'react-i18next';

import CONSTANTS from './modules/CONSTANTS.json'
import { sendRequest } from './modules/requests'

import ProtectedRoute from './components/ProtectedRoute';
import Navbar from './components/Navbar';
import Homepage from './content/Home';
import Login from './content/Login';
import Logout from './content/Logout';
import Search from './content/Search';
import TestPage from './content/TestPage';
import History from './content/History';
import User from './content/User';

function App() {
  const [loggedIn, setLoggedIn] = useState(document.cookie.indexOf(CONSTANTS.JWT_COOKIE_NAME) !== -1)

  const refreshJWT = () => {
    if (loggedIn) {
      const address = `${CONSTANTS.AUTH_API_ADDRESS}/renew_token`
      sendRequest('POST', address, {}).then(() => {
        //try to refresh jwt every half hour
        setTimeout(function () { refreshJWT() }, 1800000)
      })
    }
  }
  setTimeout(function () { refreshJWT() }, 3000)

  const postLogIn = () => {
    setLoggedIn(true)
  }
  const postLogOut = () => {
    setLoggedIn(false)
  }

  return (
    <div className={styles.App}>
      <I18nextProvider i18n={i18n}>
        <div className={styles.content}>
          <Router>
            <Navbar loggedIn={loggedIn}/>

            <Switch>
              <Route exact path='/'>
                <Homepage />
              </Route>
              <Route path='/test_page'>
                <TestPage />
              </Route>
              <Route path='/history'>
                <History />
              </Route>
              <Route path='/search'>
                <Search />
              </Route>
              <Route path='/login'>
                <Login
                  postLogIn={postLogIn}
                />
              </Route>
              <Route path='/logout'>
                <Logout
                  postLogOut={postLogOut}
                />
              </Route>
              {/* Protected Routes */}
              <Route path='/user'>
                <ProtectedRoute
                  authenticated={loggedIn}
                  component={
                    <User />
                  }
                />
              </Route>
            </Switch>
          </Router>
        </div>
      </I18nextProvider>
    </div>
  );
}

export default App;
