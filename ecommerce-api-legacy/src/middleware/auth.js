const userModel = require('../models/user');

const tokenRequired = async (req, res, next) => {
    const authHeader = req.headers['authorization'];
    if (!authHeader) {
        return res.status(401).json({ erro: 'Token de autorização ausente' });
    }

    try {
        const token = authHeader.replace('Bearer ', '');
        const userId = parseInt(token.replace('fake-jwt-token-', ''), 10);
        
        if (isNaN(userId)) {
            return res.status(401).json({ erro: 'Token inválido' });
        }

        const user = await userModel.getById(userId);
        if (!user) {
            return res.status(401).json({ erro: 'Acesso negado' });
        }
        
        req.user = user;
        next();
    } catch (err) {
        res.status(401).json({ erro: 'Token inválido' });
    }
};

module.exports = {
    tokenRequired
};
