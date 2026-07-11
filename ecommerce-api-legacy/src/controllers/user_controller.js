const userModel = require('../models/user');
const enrollmentModel = require('../models/enrollment');

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
    deleteUser
};
