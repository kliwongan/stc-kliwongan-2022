import React, { useEffect, useState } from 'react';
import { Link } from "react-router-dom";
import axios from 'axios';

function ItemsDisplay(props) {

    const printItems = (props) => {
        const { items } = props;

        if (items.length > 0) {
            return (
                items.map((item, index) => {
                    console.log(item);
                    return (
                        <div class="row shadow-lg p-3 mb-5 bg-white rounded">
                            <div class="col-sm-6" className="item" key={item.id}>
                                <div className='item' key={item.id}>
                                    <h3 className="item_title">Item name: {item.title}</h3>
                                    <p className="item_qty">Quantity: {item.quantity}</p>
                                    <p className="item_desc">Description: {item.description}</p>
                                </div>
                            </div>

                            <div class="col-sm-6" className="buttons">
                                <div class="row">
                                    <div class="col-sm-2">
                                        <Link to="/update" state = {{
                                            id: item.id,
                                            title: item.title,
                                            quantity: item.quantity,
                                            description: item.description
                                        }}>Update</Link>
                                    </div>

                                    <div class="col-sm-2">
                                        <Link to="/delete" state = {{
                                            "id": item.id,
                                        }}>Delete</Link>
                                    </div>
                                </div>
                            </div>
                        </div>
                    )
                })
            )
        } else {
            return (<h3>No items have been created yet, click <a href="/create">here</a> to create some!</h3>)
        }
    }

    return (
        <>
            {printItems(props)}
        </>
    )
}

export default function ReadItems() {

    const [items, getItems] = useState('');

    const url = "http://localhost:8000/";

    useEffect(() => {
        console.log("Getting all items");
        getAllItems();
    }, []);
    const getAllItems = () => {
        axios.get(`${url}items`)
            .then((response) => {
                const items = response.data
                getItems(items);
            })
            .catch(error => console.error(`Logged error: ${error}`));
    }

    return (<ItemsDisplay items={items} />)
}