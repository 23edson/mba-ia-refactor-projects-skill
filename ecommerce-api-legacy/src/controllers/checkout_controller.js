const db = require('../../database');
const userModel = require('../models/user');
const courseModel = require('../models/course');
const enrollmentModel = require('../models/enrollment');
const paymentModel = require('../models/payment');
const auditLogModel = require('../models/audit_log');
const bcrypt = require('bcryptjs');
const { logAndCache } = require('../utils');

async function checkout({ name, email, password, courseId, cardNumber }) {
    if (!name || !email || !courseId || !cardNumber) {
        const err = new Error("Bad Request");
        err.name = "ValidationError";
        throw err;
    }

    const course = await courseModel.getById(courseId);
    if (!course) {
        const err = new Error("Curso não encontrado");
        err.name = "NotFoundError";
        throw err;
    }

    let user = await userModel.getByEmail(email);
    let userId;

    if (!user) {
        const passHash = await bcrypt.hash(password || "123456", 10);
        userId = await userModel.create(name, email, passHash);
    } else {
        userId = user.id;
    }

    await db.run("BEGIN TRANSACTION");
    try {
        const status = cardNumber.startsWith("4") ? "PAID" : "DENIED";

        if (status === "DENIED") {
            const err = new Error("Pagamento recusado");
            err.name = "PaymentError";
            throw err;
        }

        const enrollmentId = await enrollmentModel.create(userId, courseId);
        await paymentModel.create(enrollmentId, course.price, status);
        await auditLogModel.create(`Checkout curso ${courseId} por ${userId}`);

        await db.run("COMMIT");

        logAndCache(`last_checkout_${userId}`, course.title);

        return { enrollmentId };
    } catch (error) {
        await db.run("ROLLBACK");
        throw error;
    }
}

module.exports = {
    checkout
};
