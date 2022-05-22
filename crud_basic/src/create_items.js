import { Navigate, useNavigate } from 'react-router-dom';
import axios from 'axios';
import Navbar from './navbar';


function CreateItem(name, desc, qty) {

    const url = "http://localhost:8000/";

    let request = {
        "title": name,
        "quantity": qty,
        "description": desc
    };

    axios.post(`${url}items/`, request
    ).then((response) => {
        console.log(response)
    }).catch(error => console.error(`Logged error: ${error}`));
}

function CreateItemForm() {

    let title = "";
    let desc = "";
    let qty = 0;

    let navigate = useNavigate();
    
    const navigateHome = () => {
        let path = "/";
        navigate(path);
    }

    const handleSubmit = () => {
        CreateItem(title, desc, qty);
        navigateHome();
    }

    return (
        <div class="container">
            <Navbar/>
            <h2>Create an item</h2>

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

export default CreateItemForm;