import React, { useState } from 'react';
import { useEffect } from 'react';
import { DataGrid } from '@mui/x-data-grid';
import {Box, IconButton, Typography} from '@mui/material';
import AddShoppingCartIcon from '@mui/icons-material/AddShoppingCart';
import { width } from '@mui/system';
import {Modal} from "@mui/material";
const style = {
    position: 'absolute',
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
    width: 400,
    bgcolor: 'background.paper',
    border: '2px solid #000',
    boxShadow: 24,
    p: 4,
};

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
    const [open, setOpen] = React.useState(false);
    const [bookData, setBookData] = useState()
    const handleOpen = (params, event) => {
        setOpen(true);
        setBookData(`Title: ${params["row"]["title"]} \n ISBN:${params["row"]["isbn"]}`);
    }
    const handleClose = () => setOpen(false);

    useEffect(() => {
        fetch("http://localhost:8000/api/bookcollection/books/")
            .then((response) => response.json())
            .then((books) => {
                let i = 0;
                books.forEach(book => {
                    book["id"] = i;
                    i++;
                    /* using HATEOAS!!*/
                    fetch(`http://localhost:8000${book["links"]["authors"]["href"]}`)
                        .then((response) => response.json())
                        .then((authors) => {
                            let authorArray =[];
                            authors.forEach(author => {
                                let {first_name, last_name} = author;
                                authorArray.push({
                                    'first_name': first_name,
                                    'last_name': last_name
                                })
                            })

                            book["authors"] = authorArray;
                        });
                });
                setData(books);
                console.log(books);
            });
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
                          onRowClick={handleOpen}
                />
            </div>

            <Modal
                open={open}
                onClose={handleClose}
                aria-labelledby="modal-modal-title"
                aria-describedby="modal-modal-description"
            >
                <Box sx={style}>
                    <Typography id="modal-modal-title" variant="h6" component="h2">
                        Text in a modal
                    </Typography>
                    <Typography id="modal-modal-description" sx={{ mt: 2 }}>
                        {bookData}
                    </Typography>
                </Box>
            </Modal>
        </div>
    );
}

export default BookList;