import React from 'react';
import { Switch, Route } from 'react-router-dom';
import App from "./App"

const Main = () => {
    return (
        <Switch>
            <Route exact path = '/' component = {App}></Route>
            <Route exact path = '/create' component = {App}></Route>
            <Route exact path = '/deleted' component = {App}></Route>
        </Switch>
    )
}

export default Main;