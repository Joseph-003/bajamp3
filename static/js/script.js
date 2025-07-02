document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');
    const input = document.querySelector('input[name="url"]');

    form.addEventListener('submit', function (e) {
        const url = input.value.trim();
        const valid = /^https?:\/\/(www\.)?youtube\.com\/watch\?v=|youtu\.be\//.test(url);

        if (!valid) {
            e.preventDefault();
            alert("❌ Por favor, ingresa un enlace válido de YouTube.");
        } else {
            // Puedes mostrar una animación de carga aquí
            console.log("Enviando...");
        }
    });
});
