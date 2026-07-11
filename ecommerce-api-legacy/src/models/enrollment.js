const db = require('../../database');

async function create(userId, courseId) {
    const result = await db.run(
        "INSERT INTO enrollments (user_id, course_id) VALUES (?, ?)",
        [userId, courseId]
    );
    return result.lastID;
}

async function countByUserId(userId) {
    const row = await db.get("SELECT COUNT(*) as count FROM enrollments WHERE user_id = ?", [userId]);
    return row ? row.count : 0;
}

module.exports = {
    create,
    countByUserId
};
