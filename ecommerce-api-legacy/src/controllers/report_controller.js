const courseModel = require('../models/course');

async function getFinancialReport() {
    const rows = await courseModel.getFinancialReport();
    const coursesMap = {};

    for (const row of rows) {
        if (!coursesMap[row.courseId]) {
            coursesMap[row.courseId] = {
                course: row.courseTitle,
                revenue: 0,
                students: []
            };
        }

        if (row.enrollmentId !== null) {
            const isPaid = row.paymentStatus === 'PAID';
            const paidAmount = isPaid ? row.paymentAmount : 0;
            coursesMap[row.courseId].revenue += paidAmount;
            coursesMap[row.courseId].students.push({
                student: row.userName || 'Unknown',
                paid: row.paymentAmount || 0
            });
        }
    }

    return Object.values(coursesMap);
}

module.exports = {
    getFinancialReport
};
