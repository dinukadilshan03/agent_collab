const express = require('express');
const cors = require('cors');
const axios = require('axios');
require('dotenv').config();

const app = express();
app.use(cors());
app.use(express.json());

app.post('/api/agent', async (req, res) => {
  try {
    const response = await axios.post(`${process.env.AGENT_API_URL}/agent`, req.body);
    res.json(response.data);
  } catch (error) {
    res.status(500).json({ error: 'Agent server error' });
  }
});

app.listen(3001, () => console.log('Backend running on port 3001'));
