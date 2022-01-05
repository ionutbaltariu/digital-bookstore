import React, { useState } from 'react';
import { useEffect } from 'react';
import { DataGrid } from '@mui/x-data-grid';
import { IconButton, Typography } from '@mui/material';
import AddShoppingCartIcon from '@mui/icons-material/AddShoppingCart';
import Card from '@mui/material/Card';
import { width } from '@mui/system';


const columns = [
    { field: 'isbn', headerName: 'ISBN', flex: 0.5 },
    {
        field: 'title',
        headerName: 'Book Title',
        flex: 1,
        editable: false,
    },
    {
        field: 'genre',
        headerName: 'Genre',
        flex: 1,
        editable: false,
    },
    {
        field: 'publisher',
        headerName: 'Publisher',
        flex: 1,
        editable: false,
    },
    {
        field: 'price',
        headerName: 'Price',
        type: 'number',
        flex: 0.3,
        editable: false,
    },
    {
        field: 'stock',
        headerName: 'Stock',
        flex: 0.3,
        editable: false,
    },
    {
        field: 'year_of_publishing',
        headerName: 'Year of publishing',
        flex: 0.6,
        editable: false,
    },
    {
        field: "actions",
        headerName: "",
        sortable: false,
        flex: 0.2,
        disableClickEventBubbling: true,
        renderCell: (params) => {
            return (
                <IconButton
                    color="primary"
                    aria-label="add to shopping cart"
                    onClick={() => {
                        console.log(params);
                    }}
                >
                    <AddShoppingCartIcon />
                </IconButton>
            );
        }
    }
];

function BookList() {
    const [data, setData] = useState([]);

    useEffect(() => {
        fetch("http://localhost:8000/api/bookcollection/books/")
            .then((response) => response.json())
            .then((books) => {
                let i = 0;
                books.forEach(book => {
                    book["id"] = i;
                    i++;
                });
                setData(books);
                console.log(books);
            });

        // AuthModule dummy request 
        const body = `<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"xmlns:gs="http://pos.examples.soap.stateless/Auth">"><soapenv:Header/><soapenv:Body><gs:loginRequest><gs:name>user</gs:name><gs:password>password</gs:password></gs:loginRequest></soapenv:Body></soapenv:Envelope>`;

        fetch("http://localhost:8080/sample", {
            body: body,
            method: 'POST',
            headers: {
                'Content-Type': 'text/xml'

            },
            mode: 'cors',
        })
            .then((response) => console.log(response));
    }, []);

    return (
        <div className="wrapper">
            <Typography variant="h4" gutterBottom component="div" align='center' paddingBottom={2}>
                Available Books
            </Typography>
            <div style={{
                height: '50%', width: '70%', position: 'absolute', left: '50%', top: '50%',
                transform: 'translate(-50%, -50%)'
            }}>
                <DataGrid style={{ borderColor: 'black' }}
                    rows={data}
                    columns={columns}
                    disableSelectionOnClick
                />
            </div>
        </div>
    );
}

export default BookList;