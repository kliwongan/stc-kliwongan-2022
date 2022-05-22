import { useLocation, useNavigate } from 'react-router-dom'
import axios from 'axios';
import Navbar from './navbar';

function UpdateItem(id, name, desc, qty) {

    const url = "http://localhost:8000/";

    let request = {
        "title": name,
        "quantity": qty,
        "description": desc
    };

    console.log("Request to be sent", request);

    axios.put(`${url}items/${id}`, request
    ).then((response) => {
        console.log(response)
    }).catch(error => console.error(`Logged error: ${error}`));
}

function UpdateItemForm() {

    let navigate = useNavigate();
    
    const navigateHome = () => {
        let path = "/";
        navigate(path, {state: {"update": 1}});
    }

    const location = useLocation()

    // If we are not redirected from the main page
    // or if the state variable no longer exists
    // we return to the homepage
    if (location.state === null) {
        navigateHome()
    }

    const from = location.state;

    // Get the values of the state variable
    const item_id = from.id
    let title = from.title;
    let desc = from.description;
    let qty = from.quantity;

    const handleSubmit = () => {
        UpdateItem(item_id, title, desc, qty);
        navigateHome()
    }

    return (
        <div class="container">
            <Navbar/>
            <h2>Update Item</h2>

            <form onSubmit={handleSubmit}>
                <div class="form-group">
                    <label for="Title">Title</label>
                    <input class="form-control" id="exampleFormControlInput1" placeholder={title} 
                    onChange = {(e) => {title = e.target.value}}/>
                </div>
                <div class="form-group">
                    <label for="exampleFormControlSelect1">Quantity: </label>
                    <input type="number" id="replyNumber" min="0" step="1" data-bind="value:replyNumber" 
                    placeholder = {qty} onChange = {(e) => {qty = e.target.value}}/>
                </div>
                <div class="form-group">
                    <label for="exampleFormControlTextarea1">Description</label>
                    <textarea class="form-control" id="exampleFormControlTextarea1" rows="3" placeholder={desc}
                    onChange = {(e) => {desc = e.target.value}}></textarea>
                </div>

                <input type="submit" value="Submit" />
            </form>
        </div>
    )
}

export default UpdateItemForm;