import logo from './logo.svg';
import './App.css';
import BookList from './BookList/BookList';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import React, { useState } from 'react';
import Login from './Login/Login';
import Card from '@mui/material/Card';
import { blue, red } from '@mui/material/colors';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { Typography } from '@mui/material';

const theme = createTheme({
    palette: {
        primary: {
            main: blue[500],
        },
    },
});


function App() {
    const [token, setToken] = useState();

    return (
        <div className="wrapper">
            <ThemeProvider theme={theme}>
                <h1 style={{ textAlign: 'center' }}></h1>
                <Typography variant="h3" gutterBottom component="div" align='center'>
                    Digital Bookstore
                </Typography>
                <BrowserRouter>
                    <Routes>
                        <Route path='/books' element={<BookList />} />
                    </Routes>
                </BrowserRouter>
            </ThemeProvider>

        </div>
    );
}

export default App;
