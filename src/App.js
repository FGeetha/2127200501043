import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Switch, Route, Link } from 'react-router-dom';
import axios from 'axios';
import TrainList from './components/TrainList';
import TrainDetails from './components/TrainDetails';

function App() {
  const [trains, setTrains] = useState([]);

  useEffect(() => {
    const fetchTrains = async () => {
      try {
        const response = await axios.get('/api/trains');
        setTrains(response.data);
      } catch (error) {
        console.error('Error fetching trains:', error);
      }
    };

    fetchTrains();
  }, []);

  return (
    <Router>
      <div>
        <nav>
          <ul>
            <li>
              <Link to="/">All Trains</Link>
            </li>
          </ul>
        </nav>

        <Switch>
          <Route exact path="/">
            <TrainList trains={trains} />
          </Route>
          <Route path="/train/:id">
            <TrainDetails />
          </Route>
        </Switch>
      </div>
    </Router>
  );
}

export default App;
