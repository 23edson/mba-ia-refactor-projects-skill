const express = require('express');
const config = require('../config');
const database = require('../database');

const checkoutRoutes = require('./routes/checkout_routes');
const reportRoutes = require('./routes/report_routes');
const userRoutes = require('./routes/user_routes');
const errorHandler = require('./middleware/errorHandler');

const app = express();
app.use(express.json());

app.use('/api', checkoutRoutes);
app.use('/api', reportRoutes);
app.use('/api', userRoutes);

app.use(errorHandler);

(async () => {
    try {
        await database.initDb();
        app.listen(config.port, () => {
            console.log(`Frankenstein LMS rodando na porta ${config.port}...`);
        });
    } catch (err) {
        console.error('Falha ao inicializar o banco de dados:', err);
        process.exit(1);
    }
})();

module.exports = app;
