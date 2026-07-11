module.exports = (err, req, res, next) => {
    if (err.name === 'ValidationError' || err.name === 'PaymentError') {
        return res.status(400).json({ erro: err.message });
    }
    if (err.name === 'NotFoundError') {
        return res.status(404).json({ erro: err.message });
    }
    console.error('[SERVER ERROR]', err);
    res.status(500).json({ erro: 'Erro interno' });
};
