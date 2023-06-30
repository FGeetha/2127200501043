import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { Typography } from '@mui/material';
import axios from 'axios';

const TrainDetails = () => {
  const { id } = useParams();
  const [train, setTrain] = useState(null);

  useEffect(() => {
    const fetchTrainDetails = async () => {
      try {
        const response = await axios.get(`/api/trains/${id}`);
        setTrain(response.data);
      } catch (error) {
        console.error('Error fetching train details:', error);
      }
    };

    fetchTrainDetails();
  }, [id]);

  if (!train) {
    return <Typography variant="h6">Loading...</Typography>;
  }

  return (
    <div>
      <Typography variant="h4" gutterBottom>
        Train {train.trainNumber}
      </Typography>
      <Typography variant="body1" gutterBottom>
        Departure Time: {train.departureTime}
      </Typography>
      <Typography variant="body1" gutterBottom>
        Delay: {train.delayedBy} minutes
      </Typography>
      <Typography variant="body1" gutterBottom>
        Seat Availability:
      </Typography>
      <ul>
        {Object.entries(train.seatsAvailable).map(([coach, availability]) => (
          <li key={coach}>
            {coach}: {availability} seats
          </li>
        ))}
      </ul>
      <Typography variant="body1" gutterBottom>
        Prices:
      </Typography>
      <ul>
        {Object.entries(train.price).map(([coach, price]) => (
          <li key={coach}>
            {coach}: ${price}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default TrainDetails;

