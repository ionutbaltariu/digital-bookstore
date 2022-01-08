import { React, useEffect, useState } from 'react';
import { Button, IconButton } from '@mui/material';
import PropTypes from 'prop-types';
import ArrowLeftIcon from '@mui/icons-material/ArrowLeft';
import { DataGrid } from '@mui/x-data-grid';
import './ShoppingCart.css';
import DeleteIcon from '@mui/icons-material/Delete';
import RemoveIcon from '@mui/icons-material/Remove';

export default function ShoppingCart({ setInCart }) {
    const [cartItems, setCartItems] = useState([]);

    useEffect(() => {
        setCartItems(JSON.parse(localStorage.getItem("shoppingCartItems")).map((x, i) => {
            x["id"] = i;
            return x;
        }))
    }, []);

    const columns = [
        { field: 'title', headerName: 'Book', flex: 1, editable: false },
        { field: 'number', headerName: 'Number', flex: 0.3, editable: false },
        {
            field: "actions", headerName: "", sortable: false, flex: 0.2,
            renderCell: (params) => {
                return (
                    <div>
                        <IconButton
                            color="primary"
                            aria-label="remove one item from shopping card"
                            type='button'
                            onClick={(e) => handleDecrease(params)}
                        >
                            <RemoveIcon></RemoveIcon>
                        </IconButton>
                        <IconButton
                            color="primary"
                            aria-label="delete to shopping cart"
                            type='button'
                            onClick={(e) => handleDelete(params)}
                        >
                            <DeleteIcon></DeleteIcon>
                        </IconButton>
                    </div>

                );
            }
        }
    ];

    const handleDecrease = (params) => {
        const existing = cartItems.filter((x) => {
            return x["isbn"] == params["row"]["isbn"];
        })

        existing[0]["number"]--;

        const newItems = cartItems.filter((x) => {
            return x["number"] !== 0;
        }).map((x, i) => {
            x["id"] = i;
            return x;
        });
        localStorage.setItem("shoppingCartItems", JSON.stringify(newItems));
        setCartItems(newItems);
    }

    const handleDelete = (params) => {
        const newItems = cartItems.filter((x) => {
            return x["isbn"] != params["row"]["isbn"];
        }).map((x, i) => {
            x["id"] = i;
            return x;
        });
        localStorage.setItem("shoppingCartItems", JSON.stringify(newItems));
        setCartItems(newItems);
    }

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
            <div className='vertically-centered cart'>
                <DataGrid style={{ borderColor: 'black', backgroundColor: 'white' }}
                    columns={columns}
                    rows={cartItems}
                    disableSelectionOnClick
                />
                <div className='order-btn'>
                    <Button
                        sx={{
                            marginTop: '1%',
                        }}
                        variant="contained"
                        disableElevation
                        onClick={() => {
                            let orderedBooks = [];
                            cartItems.forEach(item => {
                                orderedBooks.push({
                                    'isbn': item['isbn'],
                                    'quantity': item['number']
                                });
                            });

                            const body = JSON.stringify({
                                "user": "user",
                                "books": orderedBooks
                            })
                            console.log(body);
                            fetch("http://localhost:8001/api/orders", {
                                body: body,
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/json'
                                },
                            })
                                .then((response) => console.log(response))
                                .then(() => {
                                    localStorage.setItem("shoppingCartItems", JSON.stringify([]));
                                    setCartItems([]);
                                });

                            console.log(cartItems);
                        }}
                    >
                        Send Order
                    </Button>
                </div>
            </div>
        </div>
    );
}

ShoppingCart.propTypes = {
    setInCart: PropTypes.func.isRequired
}