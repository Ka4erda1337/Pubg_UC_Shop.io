document.getElementById("supportForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const data = {
    username: document.getElementById("username").value,
    email: document.getElementById("email").value,
    message: document.getElementById("message").value
  };

  const res = await fetch("/api/send", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  });

  if (res.ok) {
    alert("Ваше сообщение успешно отправлено!");
    e.target.reset();
  }
});
