function randomCode(length) {
    const characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    let generatedString = '';

    for (let i = 0; i < length; i++) {
        const randomIndex = Math.floor(Math.random() * characters.length);
        generatedString += characters.charAt(randomIndex);
    }

    let input = document.getElementById("id_short");
    input.value = generatedString;

    return generatedString;
}