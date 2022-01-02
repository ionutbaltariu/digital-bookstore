import logo from './logo.svg';
import './App.css';
import BookList from './BookList/BookList';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import React, { useState } from 'react';
import Login from './Login/Login';

function App() {
  const [token, setToken] = useState();

  if(!token) {
    return <Login setToken={setToken} />
  }

  return (
    <div className="wrapper">
      <h1>Digital Bookstore</h1>
      <BrowserRouter>
        <Routes>
          <Route path='/books' element={<BookList />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
