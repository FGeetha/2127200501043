const express = require('express');
const app = express();
const port = 5000;

const trainData = require('./trainData.json');

app.get('/api/trains', (req, res) => {
  res.json(trainData);
});

app.get('/api/trains/:id', (req, res) => {
  const { id } = req.params;
  const train = trainData.find((train) => train.trainNumber === id);
  res.json(train);
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
