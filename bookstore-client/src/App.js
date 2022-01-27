import './App.css';
import BookList from './BookList/BookList';
import ShoppingCart from './ShoppingCart/ShoppingCart';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import React, { useState } from 'react';
import Login from './Login/Login';
import { blue, red } from '@mui/material/colors';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { useEffect } from 'react';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { Button } from '@mui/material';

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
    const [inCart, setInCart] = useState(false);

    useEffect(() => {
        if (localStorage.getItem("shoppingCartItems") === null) {
            localStorage.setItem("shoppingCartItems", JSON.stringify([]));
        }

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
                    else {
                        setToken(jwt);
                    }
                })
        }

    }, []);

    if (!token && window.location.pathname !== '/books') {
        return <Login setToken={setToken} />
    }

    if (inCart) {
        return <ShoppingCart setInCart={setInCart}></ShoppingCart>
    }

    return (
        <div className="wrapper">
            <ToastContainer></ToastContainer>
            <Button
                style={{
                    marginRight: '1%',
                    marginTop: '1%',
                    float: 'right'
                }}
                variant="contained"
                disableElevation
                onClick={() => {
                    setInCart(!inCart);
                    console.log(inCart);
                }}
            >
                Shopping Cart
            </Button>
            {/* react's way of conditional */}
            {token ? (
                <div>
                    <Button
                        style={{
                            marginLeft: '1%',
                            marginTop: '1%',
                            float: 'left'
                        }}
                        variant="contained"
                        disableElevation
                        onClick={() => {
                            setToken(undefined);
                            localStorage.setItem("token", undefined);
                        }}
                    >
                        Logout
                    </Button>
                </div>
            ) : (<span></span>)}
            <ThemeProvider theme={theme}>

                <BrowserRouter>
                    <Routes>
                        <Route path='/' element={<BookList />} />
                        <Route path='/books' element={<BookList />} />
                    </Routes>
                </BrowserRouter>
            </ThemeProvider>
        </div>
    );
}

export default App;