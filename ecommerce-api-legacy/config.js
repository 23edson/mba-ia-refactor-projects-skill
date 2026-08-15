require('dotenv').config();

module.exports = {
    port: process.env.PORT || 3000,
    dbPath: process.env.DATABASE_PATH || ':memory:',
    dbUser: process.env.DB_USER,
    dbPass: process.env.DB_PASS,
    paymentGatewayKey: process.env.PAYMENT_GATEWAY_KEY,
    smtpUser: process.env.SMTP_USER,
    secretKey: process.env.JWT_SECRET || process.env.SECRET_KEY || 'minha-chave-super-secreta-123'
};
