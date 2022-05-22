import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Navbar from './navbar';
import { Navigate, useNavigate } from 'react-router-dom';

function PrintDeletedItems(props) {

    let navigate = useNavigate();
    
    const navigateHome = () => {
        let path = "/";
        navigate(path);
    }

    const undeleteItem = (id) => {

        let new_item = null;

        const url = "http://localhost:8000/";

        axios.post(`${url}deleted/${id}`)
            .then((response) => {
                new_item = response;
                console.log(response);
            })
            .catch(error => console.error(`Logged error: ${error}`));
        
        console.log(`Undelete success!`);
        // Timeout because useEffect keeps making the GET before the POST request
        setTimeout(100);
        navigateHome();
    }

    const printItems = (props) => {
        const { items } = props;

        if (items.length > 0) {
            return (
                items.map((item, index) => {
                    console.log(item);

                    // Add create, delete and update buttons here
                    // "gridify" the output here
                    return (
                        <div class="row shadow-lg p-3 mb-5 bg-white rounded">
                            <div class="col-sm-6" className="item" key={item.id}>
                                <div className='item' key={item.id}>
                                    <h3 className="item_title">Item name: {item.title}</h3>
                                    <p className="item_qty">Quantity: {item.quantity}</p>
                                    <p className="item_desc">Description: {item.description}</p>
                                    <p className="item_deleted_comment">Deletion comment: {item.comment}</p>
                                </div>
                            </div>

                            <div class="col-sm-6" className="buttons">
                                <div class="row">
                                    <div class="col-sm-4">
                                        <button type="button" class="btn btn-primary"
                                            onClick={() => undeleteItem(item.id)}>Undelete</button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    )
                })
            )
        } else {
            return (<h3>No items have been deleted yet</h3>)
        }
    }

    return (
        <>
            {printItems(props)}
        </>
    )
}

function DisplayDeletedItems() {

    const [items, getItems] = useState('');

    const url = "http://localhost:8000/";

    useEffect(() => {
        getAllItems();
    }, []);
    const getAllItems = () => {
        axios.get(`${url}deleted`)
            .then((response) => {
                const items = response.data
                getItems(items);
            })
            .catch(error => console.error(`Logged error: ${error}`));
    }

    return (<PrintDeletedItems items={items} />)
}

export default function Undelete() {
    return (
        <div class="container">
            <Navbar />
            <div class="grid grid-cols-4">
                <DisplayDeletedItems />
            </div>
        </div>
    )
}