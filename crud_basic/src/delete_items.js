import { useLocation, useNavigate } from 'react-router-dom'
import axios from 'axios';
import Navbar from './navbar';

function DeleteItem(id, comment) {

    const url = "http://localhost:8000/";

    const DeleteSpecificItem = () => {
        axios.delete(`${url}items/${id}?comment=${comment}`
        ).then((response) => {
            console.log(response);
        }).catch(error => console.error(`Logged error: ${error}`));
    }
    DeleteSpecificItem();
}

function DeleteItemForm() {

    let navigate = useNavigate();

    const navigateHome = () => {
        let path = "/";
        navigate(path);
    }

    const location = useLocation();

    // If we are not redirected from the main page
    // or if the state variable no longer exists
    // we return to the homepage
    if (location.state === null) {
        navigateHome();
    }

    const from = location.state;

    // Get the values of the state variable
    const item_id = from.id
    let comment = "";

    const handleSubmit = () => {
        DeleteItem(item_id, comment);
        // Timeout because useEffect keeps making the GET before the DELETE request
        setTimeout(100);
        navigateHome();
    }

    return (
        <div class="container">
            <Navbar />
            <h2>Delete Item</h2>

            <form onSubmit={handleSubmit}>
                <div class="form-group">
                    <label for="exampleFormControlTextarea1">Deletion comment</label>
                    <textarea class="form-control" id="exampleFormControlTextarea1" rows="3" placeholder={comment}
                        onChange={(e) => { comment = e.target.value }}></textarea>
                </div>

                <input type="submit" value="Submit"/>
            </form>
        </div>
    )
}

export default DeleteItemForm;