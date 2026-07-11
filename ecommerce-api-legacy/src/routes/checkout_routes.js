const express = require('express');
const router = express.Router();
const checkoutController = require('../controllers/checkout_controller');

router.post('/checkout', async (req, res, next) => {
    try {
        const { usr, eml, pwd, c_id, card } = req.body;
        
        const result = await checkoutController.checkout({
            name: usr,
            email: eml,
            password: pwd,
            courseId: c_id,
            cardNumber: card
        });
        
        res.status(200).json({ msg: "Sucesso", enrollment_id: result.enrollmentId });
    } catch (error) {
        next(error);
    }
});

module.exports = router;
