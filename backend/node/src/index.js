const express = require('express');
const { Pool } = require('pg');

const app = express();
const port = process.env.PORT || 8001;

const pool = new Pool({
  connectionString:
    process.env.DATABASE_URL ||
    'postgresql://postgres:postgres@db:5432/easyhomemg',
});

app.get('/health', (req, res) => {
  res.json({ status: 'ok', service: 'node-api' });
});

app.get('/db', async (req, res) => {
  try {
    const result = await pool.query('SELECT 1 AS ok');
    res.json({ service: 'node-api', db: result.rows[0] });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.listen(port, () => {
  console.log(`Node API listening on port ${port}`);
});
