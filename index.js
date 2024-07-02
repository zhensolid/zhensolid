// index.js
function generateSerialNumber() {
    const now = new Date();
    const year = now.getFullYear();
    const month = (now.getMonth() + 1).toString().padStart(2, "0");
    const day = now.getDate().toString().padStart(2, "0");
    const hour = now.getHours().toString().padStart(2, "0");
    const minute = now.getMinutes().toString().padStart(2, "0");
    const second = now.getSeconds().toString().padStart(2, "0");
    const random = Math.floor(Math.random() * 1000)
        .toString()
        .padStart(3, "0");

    // 生成格式: YYYYMMDDHHMMSSRRR
    return `${year}${month}${day}${hour}${minute}${second}${random}`;
}

module.exports = generateSerialNumber;
