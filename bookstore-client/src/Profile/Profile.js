import { useEffect } from "react";
import React, { useState } from 'react';
import './Profile.css';
import PropTypes from 'prop-types';
import { Button } from "@mui/material";
import { Typography } from "@mui/material";

export default function Profile({ setInProfile }) {
    const [orders, setOrders] = useState([])

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
                console.log(orders);
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
                <div className="order-container">
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
            </div>
        </div>

    )
}

Profile.propTypes = {
    setInProfile: PropTypes.func.isRequired
}
