import './App.css';
import ReadItems from './read_items';
import Navbar from './navbar';

function App() {
  return (
    <div class="container">
      <Navbar />
      <div class="grid grid-cols-4">
        <ReadItems />
      </div>
    </div>
  )
}

export default App;
