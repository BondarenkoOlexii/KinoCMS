async function postData(taskId, url) {
    // Тепер ми просто використовуємо url, який дав нам Django
    fetch(url)
    .then(response => {
        if (!response.ok) {
            throw new Error(`Помилка сервера: ${response.status} за адресою ${url}`);
        }
        return response.json();
    })
    .then(data => {
        console.log("Дані з сервера:", data);

        if (data.state === "PROGRESS" && data.result) {
            document.getElementById('current-status-count').innerText = data.result.current || 0;
            document.getElementById('total-count').innerText = data.result.total || 0;
            document.getElementById('percent').innerText = (data.result.percent || 0) + "%";
        }

        if (data.state === "SUCCESS") {
            document.getElementById('current-status-count').innerText = "Успішно";
            document.getElementById('percent').innerText = "100%";
            return; // Вихід з циклу
        }

        // Продовжуємо, якщо не SUCCESS і не FAILURE
        if (data.state !== "SUCCESS" && data.state !== "FAILURE") {
            setTimeout(() => postData(taskId, url), 800);
        }
    })
    .catch(error => {
        console.error("Помилка:", error.message);
    });
}