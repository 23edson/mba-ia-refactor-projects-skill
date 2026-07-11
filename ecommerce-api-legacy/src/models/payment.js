const db = require('../../database');

async function create(enrollmentId, amount, status) {
    const result = await db.run(
        "INSERT INTO payments (enrollment_id, amount, status) VALUES (?, ?, ?)",
        [enrollmentId, amount, status]
    );
    return result.lastID;
}

module.exports = {
    create
};
