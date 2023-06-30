import React from 'react';
import { Link } from 'react-router-dom';
import { List, ListItem, ListItemText } from '@mui/material';

const TrainList = ({ trains }) => {
  return (
    <List>
      {trains.map((train) => (
        <ListItem
          key={train.trainNumber}
          button
          component={Link}
          to={`/train/${train.trainNumber}`}
        >
          <ListItemText primary={`Train ${train.trainNumber}`} />
        </ListItem>
      ))}
    </List>
  );
};

export default TrainList;
