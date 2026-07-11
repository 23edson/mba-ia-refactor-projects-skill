const db = require('../../database');

async function getById(id) {
    return db.get("SELECT * FROM courses WHERE id = ? AND active = 1", [id]);
}

async function getAll() {
    return db.all("SELECT * FROM courses");
}

async function getFinancialReport() {
    return db.all(`
        SELECT 
            c.id as courseId, 
            c.title as courseTitle, 
            e.id as enrollmentId,
            u.name as userName, 
            p.amount as paymentAmount, 
            p.status as paymentStatus
        FROM courses c
        LEFT JOIN enrollments e ON e.course_id = c.id
        LEFT JOIN users u ON u.id = e.user_id
        LEFT JOIN payments p ON p.enrollment_id = e.id
    `);
}

module.exports = {
    getById,
    getAll,
    getFinancialReport
};
