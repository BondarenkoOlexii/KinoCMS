document.addEventListener('DOMContentLoaded', function() {
    const grid = document.getElementById('hall-grid');
    const bookingForm = document.getElementById('booking-form');
    let currentAction = 'reserve'; // Тип дії за замовчуванням

    if (!grid) return;

    const url = grid.dataset.jsonUrl;
    const sessionId = grid.dataset.sessionId;
    let bookedIds = [];

    try {
        bookedIds = JSON.parse(grid.dataset.booked || "[]");
    } catch (e) {
        console.error("Помилка парсингу booked_ids. Перевір json.dumps та |safe");
    }

    // WebSocket
    let socket = null;
    if (sessionId) {
        socket = new WebSocket('ws://' + window.location.host + '/ws/booking/' + sessionId + '/');
        socket.onmessage = function(e) {
            const data = JSON.parse(e.data);
            if (data.action === 'reserve') {
                data.seats.forEach(id => {
                    const el = document.querySelector(`[data-id="${id}"]`);
                    if (el) el.className = 'seat occupied';
                });
            }
        };
    }

    // Завантаження залу
    fetch(url)
        .then(res => res.json())
        .then(data => renderHall(data))
        .catch(err => console.error("Помилка завантаження JSON:", err));

    function renderHall(data) {
        grid.innerHTML = '';
        const wrapper = document.createElement('div');
        wrapper.className = 'hall-container';

        data.rows.forEach(row => {
            const rowEl = document.createElement('div');
            rowEl.className = 'row-wrapper';

            const label = document.createElement('div');
            label.className = 'row-label';
            label.innerText = row.rowNumber;
            rowEl.appendChild(label);

            const list = document.createElement('div');
            list.className = 'seats-list';

            row.seats.forEach(seat => {
                const div = document.createElement('div');
                if (seat.isGap) {
                    div.className = 'gap';
                } else {
                    div.className = 'seat';
                    if (seat.type === 'vip') div.classList.add('vip');
                    div.innerText = seat.label;
                    div.dataset.id = seat.id;

                    if (bookedIds.includes(seat.id)) {
                        div.classList.add('occupied');
                    } else {
                        div.classList.add('available');
                        div.onclick = function() {
                            this.classList.toggle('selected');
                        };
                    }
                }
                list.appendChild(div);
            });
            rowEl.appendChild(list);
            wrapper.appendChild(rowEl);
        });
        grid.appendChild(wrapper);
    }

    // Визначаємо action перед сабмітом
    document.getElementById('reserve-btn').addEventListener('click', () => currentAction = 'reserve');
    document.getElementById('buy-btn').addEventListener('click', () => currentAction = 'buy');

    bookingForm.addEventListener('submit', function(e) {
        e.preventDefault();

        const selectedSeats = Array.from(document.querySelectorAll('.seat.selected'))
                                   .map(seat => seat.dataset.id)
                                   .filter(id => id);

        if (selectedSeats.length === 0) {
            alert("Будь ласка, виберіть місця!");
            return;
        }

        fetch(window.location.href, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            },
            body: JSON.stringify({
                'selected_seats': selectedSeats,
                'action': currentAction
            })
        })
        .then(res => res.json())
        .then(data => {
            if (data.status === 'success') {
                // Відправляємо дані в сокет, щоб інші побачили зайняті місця
                if (socket && socket.readyState === WebSocket.OPEN) {
                    socket.send(JSON.stringify({ 'action': 'reserve', 'seats': selectedSeats }));
                }

                if (data.action === 'buy') {
                    alert('Переходимо до оплати...');
                    window.open(data.redirect_url, '_blank'); // ВІДКРИВАЄМО В НОВІЙ ВКЛАДЦІ
                } else {
                    alert('Успішно заброньовано!');
                }
                location.reload();
            } else {
                alert('Помилка: ' + data.message);
            }
        });
    });
});