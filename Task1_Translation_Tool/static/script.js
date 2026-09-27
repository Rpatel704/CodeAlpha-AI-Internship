async function translateText() {
    const input = document.getElementById("inputText").value.trim();
    const source = document.getElementById("sourceLanguage").value;
    const target = document.getElementById("targetLanguage").value;
    const status = document.getElementById("status");
    const output = document.getElementById("outputText");
    const button = document.getElementById("translateButton");

    if (!input) {
        status.textContent = "Please enter some text to translate.";
        output.value = "";
        return;
    }

    button.disabled = true;
    button.textContent = "Translating...";
    status.textContent = "Translating...";

    try {
        const response = await fetch("/api/translate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                text: input,
                source: source,
                target: target
            })
        });

        const data = await response.json();

        if (data.success) {
            output.value = data.translation;
            status.textContent = "Translation completed successfully.";
        } else {
            output.value = "";
            status.textContent = data.error || "Translation failed.";
        }

    } catch (error) {
        output.value = "";
        status.textContent = "Unable to connect to the translation service.";
    } finally {
        button.disabled = false;
        button.textContent = "Translate";
    }
}
