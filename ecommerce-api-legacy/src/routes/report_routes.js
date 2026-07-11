const express = require('express');
const router = express.Router();
const reportController = require('../controllers/report_controller');
const { tokenRequired } = require('../middleware/auth');

router.get('/admin/financial-report', tokenRequired, async (req, res, next) => {
    try {
        const report = await reportController.getFinancialReport();
        res.json(report);
    } catch (error) {
        next(error);
    }
});

module.exports = router;
