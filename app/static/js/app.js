const form = document.querySelector("#question-form");
const promptInput = document.querySelector("#prompt");
const characterCount = document.querySelector("#character-count");
const typingState = document.querySelector("#typing-state");
const chatBox = document.querySelector("#chat-box");
const suggestionButtons = document.querySelectorAll("[data-prompt]");

const resizePrompt = () => {
    if (!promptInput) return;

    promptInput.style.height = "auto";
    promptInput.style.height = `${Math.min(promptInput.scrollHeight, 150)}px`;
};

const updateCharacterCount = () => {
    if (!promptInput || !characterCount) return;

    const length = promptInput.value.length;
    characterCount.textContent = `${length} / 1000`;
    characterCount.classList.toggle("has-content", length > 0);
};

suggestionButtons.forEach((button) => {
    button.addEventListener("click", () => {
        if (!promptInput) return;

        promptInput.value = button.dataset.prompt || "";
        resizePrompt();
        updateCharacterCount();
        promptInput.focus();
    });
});

promptInput?.addEventListener("input", () => {
    resizePrompt();
    updateCharacterCount();
});

promptInput?.addEventListener("keydown", (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();

        if (form?.requestSubmit && promptInput.value.trim()) {
            form.requestSubmit();
        }
    }
});

form?.addEventListener("submit", () => {
    const submitButton = form.querySelector("button[type='submit']");
    const buttonLabel = submitButton?.querySelector("span");

    if (submitButton) submitButton.disabled = true;
    if (buttonLabel) buttonLabel.textContent = "Reviewing";

    if (typingState) {
        typingState.hidden = false;
        typingState.scrollIntoView({ behavior: "smooth", block: "end" });
    }
});

window.addEventListener("load", () => {
    resizePrompt();
    updateCharacterCount();

    if (chatBox && document.querySelector(".message-list")) {
        chatBox.scrollTop = chatBox.scrollHeight;
    }
});
