import React from 'react';
import { Button } from '@mui/material';
import PropTypes from 'prop-types';
import ArrowLeftIcon from '@mui/icons-material/ArrowLeft';

export default function ShoppingCart({setInCart}) {
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
                    setInCart(false);
                }}
            >
                <ArrowLeftIcon></ArrowLeftIcon>
            </Button>
        </div>
    );
}

ShoppingCart.propTypes = {
    setInCart: PropTypes.func.isRequired
}