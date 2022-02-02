import { useEffect } from "react";
import React, { useState } from 'react';
import './Profile.css';
import PropTypes from 'prop-types';
import { Button } from "@mui/material";
import { Typography } from "@mui/material";
import { Grid } from "@mui/material";

export default function Profile({ setInProfile }) {
    const [orders, setOrders] = useState([])
    const [personalData, setPersonalData] = useState({});

    useEffect(() => {
        let jwt = localStorage.getItem("token");

        fetch("http://localhost:8002/orders", {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${jwt}`
            },
        })
            .then(async (response) => {
                setOrders(await response.json());
            })

        fetch("http://localhost:8002/user/data", {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${jwt}`
            },
        })
            .then(async (response) => {
                setPersonalData(await response.json());
            })
    }, []);

    return (
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
                    setInProfile(false);
                }}
            >
                Back
            </Button>
            <div className="profile-wrapper">
                <div className="order-container" style={{
                    marginBottom: "1%"
                }}>
                    <Grid container rowSpacing={1} columnSpacing={{ xs: 1, sm: 2, md: 3 }}>
                        <Grid item xs={6}>
                            <Typography gutterBottom component="div" align='center' paddingTop={1}>
                                First Name: {personalData["firstname"]}
                            </Typography>
                        </Grid>
                        <Grid item xs={6}>
                            <Typography gutterBottom component="div" align='center' paddingTop={1}>
                                Last Name: {personalData["lastname"]}
                            </Typography>
                        </Grid>
                        <Grid item xs={6}>
                            <Typography gutterBottom component="div" align='center' paddingTop={1}>
                                Username: {personalData["username"]}
                            </Typography>
                        </Grid>
                        <Grid item xs={6}>
                            <Typography gutterBottom component="div" align='center' paddingTop={1}>
                                Email: {personalData["email"]}
                            </Typography>
                        </Grid>
                        <Grid item xs={6}>
                            <Typography gutterBottom component="div" align='center' paddingTop={1}>
                                Birthday: {personalData["birthday"]}
                            </Typography>
                        </Grid>
                        <Grid item xs={6}>
                            <Typography gutterBottom component="div" align='center' paddingTop={1}>
                                Address: {personalData["address"]}
                            </Typography>
                        </Grid>
                    </Grid>
                </div>
                <div className="order-container">
                    {orders.length > 0 ? (
                        <div>
                            <Typography gutterBottom component="div" align='center' paddingTop={1}>
                                Your orders:
                            </Typography>

                            <ul>
                                {orders.map((order) => (
                                    <li key={order["date"]}>
                                        <h2><b>{`${order["date"].split(' ')[0]} / ${order["status"]}`}</b></h2>
                                        <ul>
                                            {order["items"].map((item) => (
                                                <li key={item["isbn"]}>
                                                    {`${item["title"]} / Quantity: ${item["quantity"]} / Total Price: ${item["price"]}`}
                                                </li>
                                            ))}
                                        </ul>
                                    </li>
                                ))}
                            </ul>
                        </div>
                    ) : (
                        <Typography gutterBottom component="div" align='center' paddingTop={1}>
                            Your have not made any orders until now!
                        </Typography>
                    )}

                </div>
            </div>
        </div>

    )
}

Profile.propTypes = {
    setInProfile: PropTypes.func.isRequired
}
