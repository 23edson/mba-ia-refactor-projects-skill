const userModel = require('../models/user');
const enrollmentModel = require('../models/enrollment');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const config = require('../../config');

async function login(email, password) {
    if (!email || !password) {
        const err = new Error("Email e senha são obrigatórios");
        err.name = "ValidationError";
        throw err;
    }

    const user = await userModel.getByEmail(email);
    if (!user) {
        const err = new Error("Credenciais inválidas");
        err.name = "ValidationError";
        throw err;
    }

    const match = await bcrypt.compare(password, user.pass);
    if (!match) {
        const err = new Error("Credenciais inválidas");
        err.name = "ValidationError";
        throw err;
    }

    const token = jwt.sign({ userId: user.id }, config.secretKey, { expiresIn: '24h' });
    
    const { pass, ...userWithoutPass } = user;

    return {
        user: userWithoutPass,
        token
    };
}

async function deleteUser(id) {
    const user = await userModel.getById(id);
    if (!user) {
        const err = new Error("Usuário não encontrado");
        err.name = "NotFoundError";
        throw err;
    }

    const enrollmentsCount = await enrollmentModel.countByUserId(id);
    if (enrollmentsCount > 0) {
        const err = new Error("Usuário possui matrículas e não pode ser removido");
        err.name = "ValidationError";
        throw err;
    }

    await userModel.deleteUser(id);
    return { msg: "Usuário deletado com sucesso" };
}

module.exports = {
    login,
    deleteUser
};
