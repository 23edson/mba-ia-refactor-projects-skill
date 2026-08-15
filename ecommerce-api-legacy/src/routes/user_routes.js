const express = require('express');
const router = express.Router();
const userController = require('../controllers/user_controller');
const { tokenRequired } = require('../middleware/auth');

router.post('/login', async (req, res, next) => {
    try {
        const { email, password } = req.body;
        const result = await userController.login(email, password);
        res.json(result);
    } catch (error) {
        next(error);
    }
});

router.delete('/users/:id', tokenRequired, async (req, res, next) => {
    try {
        const id = parseInt(req.params.id, 10);
        const result = await userController.deleteUser(id);
        res.json(result);
    } catch (error) {
        next(error);
    }
});

module.exports = router;
