document.addEventListener('DOMContentLoaded', function() {
    const grid = document.getElementById('hall-grid');
    const url = grid.dataset.jsonUrl;

    console.log("Шлях до файлу:", url);

    if (url) {
        fetch(url)
            .then(res => res.json())
            .then(data => {
                console.log("Дані отримано:", data);
                // Перевіряємо чи є дані
                if (data && data.rows) {
                    renderHall(data);
                } else {
                    console.error("JSON завантажився, але в ньому немає ключа 'rows'");
                }
            })
            .catch(err => console.error("Помилка завантаження:", err));
    }

    function renderHall(data) {
        grid.innerHTML = '';
        const wrapper = document.createElement('div');
        wrapper.className = 'hall-container';

        data.rows.forEach(row => {
            const rowEl = document.createElement('div');
            rowEl.className = 'row-wrapper';

            // Номер ряду
            const label = document.createElement('div');
            label.className = 'row-label';
            label.innerText = row.rowNumber;
            rowEl.appendChild(label);

            // Список крісел
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

                    div.onclick = function() {
                        this.classList.toggle('selected');
                    };
                }
                list.appendChild(div);
            });

            rowEl.appendChild(list);
            wrapper.appendChild(rowEl);
        });

        grid.appendChild(wrapper);
    }
});