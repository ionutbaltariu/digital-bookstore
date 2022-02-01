import React, { useState } from 'react';
import './Register.css'
import PropTypes from 'prop-types';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { Box, TextField, Button, Typography } from '@mui/material';

const notifyError = (message) => toast.error(message, {
    position: "top-center",
    autoClose: 5000,
    hideProgressBar: false,
    closeOnClick: true,
    pauseOnHover: true,
    draggable: true,
    progress: undefined,
});

const notifyInfo = (message) => toast.info(message, {
    position: "top-center",
    autoClose: 5000,
    hideProgressBar: false,
    closeOnClick: true,
    pauseOnHover: true,
    draggable: true,
    progress: undefined,
});

export default function Register({ setInRegister }) {
    const [username, setUserName] = useState();
    const [password, setPassword] = useState();
    const [firstName, setFirstName] = useState();
    const [lastName, setLastName] = useState();
    const [email, setEmail] = useState();
    const [address, setAddress] = useState();
    const [birthday, setBirthday] = useState();

    const register = () => {
        fetch("http://localhost:8002/register", {
            body: JSON.stringify({
                "firstname": firstName,
                "lastname": lastName,
                "email": email,
                "address": address,
                "birthday": birthday,
                "username": username,
                "password": password
            }),
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'

            },
        })
            .then(async (response) => {
                let resp_body = await response.json();

                if (response.ok) {
                    notifyInfo(`Successfully registered the user '${username}'. You will be redirected to the login page.`);
                    setTimeout(() => {
                        setInRegister(false);
                    }, 5000);
                }
                else if (response.status === 422) {
                    let invalid_fields = [];
                    for (const invalid_field of resp_body["detail"]) {
                        invalid_fields.push(invalid_field["loc"][1])
                    }

                    notifyError(`Please check again the following fields: ${invalid_fields.reduce((x, y) => x + ", " + y)} `)
                }
                else {
                    notifyError(`${resp_body["status"]} ${resp_body["errorMessage"]} `)
                }
            });
    }


    return (
        <div>
            <ToastContainer />
            <div className="register-card">
                <Typography variant="h5" gutterBottom component="div" align='center' paddingBottom={2}>
                    Register
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
                        id="firstname_input"
                        label="First name"
                        onChange={e => setFirstName(e.target.value)}
                    />
                    <TextField
                        id="lastname_input"
                        label="Last name"
                        onChange={e => setLastName(e.target.value)}
                    />
                    <TextField
                        id="email_input"
                        label="Email"
                        onChange={e => setEmail(e.target.value)}
                    />
                    <TextField
                        id="address_input"
                        label="Address"
                        onChange={e => setAddress(e.target.value)}
                    />
                    <TextField
                        id="date"
                        label="Birthday"
                        type="date"
                        defaultValue="2000-01-01"
                        onChange={e => setBirthday(e.target.value)}
                    />
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
                    onClick={() => register()}
                    disableElevation>
                    Register
                </Button>
            </div>
        </div>
    )
}

Register.propTypes = {
    setInRegister: PropTypes.func.isRequired
}