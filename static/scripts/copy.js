function copyLink(code, URL) {
    const generatedString = URL + code;

    navigator.clipboard.writeText(generatedString)
        .then(() => {
            console.log("Text copied to clipboard");
        })
        .catch((error) => {
            console.error("Failed to copy text to clipboard:", error);
        });
}