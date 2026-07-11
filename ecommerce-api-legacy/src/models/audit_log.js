const db = require('../../database');

async function create(action) {
    const result = await db.run(
        "INSERT INTO audit_logs (action, created_at) VALUES (?, datetime('now'))",
        [action]
    );
    return result.lastID;
}

module.exports = {
    create
};
