document.getElementById("add-slot-form").addEventListener("submit", () => {
    event.preventDefault();
    let popup = document.getElementById("info-popup");
    popup.style.display = "initial";
    popup.classList.remove("fadeOutAnimation");
    popup.classList.add("fadeInAnimation");
    }
)

function submitAddSlotForm() {
    document.getElementById("add-slot-form").submit();
    let popup = document.getElementById("info-popup");
    popup.classList.remove("fadeInAnimation");
    popup.classList.add("fadeOutAnimation");
    popup.style.display = "none";
}
