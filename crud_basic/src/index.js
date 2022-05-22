import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import './index.css';
import "jquery/dist/jquery";
import "bootstrap/dist/js/bootstrap";
import 'bootstrap/dist/css/bootstrap.min.css';
import App from './App';
import UndeleteItems from './undelete_items';
import reportWebVitals from './reportWebVitals';
import UpdateItemForm from './update_items';
import CreateItemForm from './create_items';
import DeleteItemForm from './delete_items';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <BrowserRouter>
    <Routes>
      <Route path = "/" element={<App />} />
      <Route path = "/create" element={<CreateItemForm />} />
      <Route path = "/update" element={<UpdateItemForm />} />
      <Route path = "/delete" element = {<DeleteItemForm/>} />
      <Route path = "/deleted" element={<UndeleteItems />} />
    </Routes>
  </BrowserRouter>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
