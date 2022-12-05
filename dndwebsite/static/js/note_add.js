function addNote() {
    const button = document.getElementById("note-button");
    const form = document.getElementById("add-note-form");
    const textField = document.getElementById("note-input");
    button.style.display = "none";
    form.classList.remove("hidden");
    
    textField.focus();
    return;
}