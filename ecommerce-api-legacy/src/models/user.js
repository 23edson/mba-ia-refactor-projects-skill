const db = require('../../database');

async function getByEmail(email) {
    return db.get("SELECT * FROM users WHERE email = ?", [email]);
}

async function getById(id) {
    return db.get("SELECT * FROM users WHERE id = ?", [id]);
}

async function create(name, email, passHash) {
    const result = await db.run(
        "INSERT INTO users (name, email, pass) VALUES (?, ?, ?)",
        [name, email, passHash]
    );
    return result.lastID;
}

async function deleteUser(id) {
    const result = await db.run("DELETE FROM users WHERE id = ?", [id]);
    return result.changes > 0;
}

module.exports = {
    getByEmail,
    getById,
    create,
    deleteUser
};
