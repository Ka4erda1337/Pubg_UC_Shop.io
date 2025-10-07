function sendSupport() {
    const name = document.getElementById('support-name').value.trim();
    const email = document.getElementById('support-email').value.trim();
    const message = document.getElementById('support-message').value.trim();
    const msg = document.getElementById('support-msg');

    if (name.length < 2) {
        msg.textContent = "Имя должно содержать минимум 2 символа";
        msg.style.color = "red";
        return;
    }

    const re = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
    if (!re.test(email)) {
        msg.textContent = "Введите корректный email";
        msg.style.color = "red";
        return;
    }

    if (message.length < 5) {
        msg.textContent = "Сообщение должно содержать минимум 5 символов";
        msg.style.color = "red";
        return;
    }

    const data = {
        name: name,
        email: email,
        message: message
    };

    Telegram.WebApp.sendData(JSON.stringify(data));

    msg.textContent = "Ваше обращение успешно отправлено!";
    msg.style.color = "green";

    document.getElementById('support-name').value = "";
    document.getElementById('support-email').value = "";
    document.getElementById('support-message').value = "";
}

function loadSupportForm() {
    const user = JSON.parse(localStorage.getItem('currentUser'));
    if (user) {
        document.getElementById('support-name').value = user.username;
        document.getElementById('support-email').value = user.email;
    }
}