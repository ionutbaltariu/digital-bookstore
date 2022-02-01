import React, { useState } from 'react';
import './Login.css';
import PropTypes from 'prop-types';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { Box, TextField, Button, Typography } from '@mui/material';

export default function Login({ setToken, setInRegister }) {
    const [username, setUserName] = useState();
    const [password, setPassword] = useState();

    const notify = () => toast.error('Credentials are not valid.', {
        position: "top-center",
        autoClose: 5000,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        progress: undefined,
    });


    return (
        <div className="login-wrapper">
            <ToastContainer />
            <div className='login-card'>
                <Typography variant="h5" gutterBottom component="div" align='center' paddingBottom={2}>
                    Please log in
                </Typography>
                <Box
                    component="form"
                    sx={{
                        '& > :not(style)': { m: 1, width: '25ch', height: '7ch' },
                    }}
                    noValidate
                    autoComplete="off"
                >
                    <TextField
                        id="username_input"
                        label="Username"
                        onChange={e => setUserName(e.target.value)}
                    />
                    <br></br>
                    <TextField
                        id="password_Input"
                        label="Password"
                        type="password"
                        onChange={e => setPassword(e.target.value)}
                    />
                    <br></br>
                </Box>
                <Button
                    style={{
                        marginBottom: '1%'
                    }}
                    variant="contained"
                    onClick={() => {
                        fetch("http://localhost:8002/login", {
                            body: JSON.stringify({ "username": username, "password": password }),
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'

                            },
                        })
                            .then((response) => response.json()
                                .then((resp) => {
                                    if (resp["token"]) {
                                        localStorage.setItem("token", resp["token"]);
                                        setToken(resp["token"]);
                                    }
                                    else {
                                        notify();
                                    }
                                }));
                    }}
                    disableElevation>
                    Login
                </Button>
                <Typography gutterBottom component="div" align='center' paddingTop={1}>
                    No account? Books can be viewed <a href='/books'>here</a>
                </Typography>
                <Typography gutterBottom component="div" align='center' paddingTop={1}>
                    No account? One can register <a href='#' onClick={() => setInRegister(true)}>here</a>
                </Typography>
            </div>
        </div>
    )
}

Login.propTypes = {
    setToken: PropTypes.func.isRequired,
    setInRegister: PropTypes.func.isRequired
}