import { useEffect } from "react";
import React, { useState } from 'react';
import './Profile.css';
import PropTypes from 'prop-types';
import { Button } from "@mui/material";
import { Typography } from "@mui/material";

export default function Profile({ setInProfile }) {
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
                <div className="helper">
                    <Typography gutterBottom component="div" align='center' paddingTop={1}>
                        your orders
                    </Typography>
                </div>
            </div>
        </div>

    )
}

Profile.propTypes = {
    setInProfile: PropTypes.func.isRequired
}
