const jwt = require('jsonwebtoken');
const config = require('../../config');
const userModel = require('../models/user');

const tokenRequired = async (req, res, next) => {
    const authHeader = req.headers['authorization'];
    if (!authHeader) {
        return res.status(401).json({ erro: 'Token de autorização ausente' });
    }

    try {
        const token = authHeader.replace('Bearer ', '');
        const decoded = jwt.verify(token, config.secretKey);
        const userId = decoded.userId;

        if (isNaN(userId)) {
            return res.status(401).json({ erro: 'Token inválido' });
        }

        const user = await userModel.getById(userId);
        if (!user) {
            return res.status(401).json({ erro: 'Acesso negado' });
        }
        
        req.user = user;
        next();
    } catch {
        res.status(401).json({ erro: 'Token inválido ou expirado' });
    }
};

module.exports = {
    tokenRequired
};
