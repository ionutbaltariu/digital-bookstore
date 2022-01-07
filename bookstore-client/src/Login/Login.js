import React, { useState } from 'react';
import './Login.css';
import PropTypes from 'prop-types';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { Box, TextField, Card, Button, Typography } from '@mui/material';

export default function Login({ setToken }) {
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
            <ToastContainer></ToastContainer>
            <div style={{
                height: '50%', width: '15%', position: 'absolute', left: '50%', top: '50%',
                transform: 'translate(-50%, -50%)'
            }}>
                <Card sx={{
                    textAlign: 'center',
                    minHeight: '45%',
                }}>
                    <Typography variant="h5" gutterBottom component="div" align='center' paddingBottom={2}>
                        Please log in
                    </Typography>                    <Box
                        component="form"
                        sx={{
                            '& > :not(style)': { m: 1, width: '25ch' },
                        }}
                        noValidate
                        autoComplete="off"
                    >
                        <TextField
                            id="username_input"
                            label="Username"
                            onChange={e => setUserName(e.target.value)}
                        />
                        <TextField
                            id="password_Input"
                            label="Password"
                            type="password"
                            onChange={e => setPassword(e.target.value)}
                        />
                    </Box>
                    <Button
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
                </Card>

            </div>
        </div>
    )
}

Login.propTypes = {
    setToken: PropTypes.func.isRequired
}