import logo from './logo.svg';
import './App.css';
import BookList from './BookList/BookList';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import React, { useState } from 'react';
import Login from './Login/Login';
import { blue, red } from '@mui/material/colors';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { Typography } from '@mui/material';
import { useEffect } from 'react';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const theme = createTheme({
    palette: {
        primary: {
            main: blue[500],
        },
    },
});
const notifyTokenExpired = () => toast.info('Your token has expired or is invalid. Please log in again', {
    position: "top-center",
    autoClose: 5000,
    hideProgressBar: false,
    closeOnClick: true,
    pauseOnHover: true,
    draggable: true,
    progress: undefined,
});

function App() {
    const [token, setToken] = useState();

    useEffect(() => {
        console.log(window.location.pathname);
        let jwt = localStorage.getItem("token");

        if (jwt) {
            fetch("http://localhost:8002/validate", {
                body: JSON.stringify({ "token": jwt }),
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
            })
                .then(response => {
                    if (response.status === 401) {
                        localStorage.removeItem("token");
                        notifyTokenExpired();
                    }
                    else{
                        setToken(jwt);
                    }
                })
        }

    }, []);

    if (!token && window.location.pathname !== '/books') {
        return <Login setToken={setToken} />
    }

    return (
        <div className="wrapper">
            <ToastContainer></ToastContainer>
            <ThemeProvider theme={theme}>
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