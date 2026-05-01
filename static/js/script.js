$(document).ready(function() {
    let timerInterval;

    attachClickHandlers();
    startTimerUpdates();
});

function updateTimer() {
    fetch('/get_timer')
        .then(response => response.json())
        .then(data => {
            document.getElementById('timer').textContent = data.elapsed_time;
        })
            .catch(err => console.error('Error fetching timer:', err));
}

function checkIfTimerStarted() {
    fetch('/get_timer')
        .then(response => response.json())
        .then(data => {
            if (data.running) {
                clearInterval(checkTimerInterval);
                timerInterval = setInterval(updateTimer, 1000);
                updateTimer();
            } else {
                console.log("Timer not running yet. Waiting for the first move.");
            }
        })
            .catch(err => console.error('Error fetching initial timer state:', err));
}

function startTimerUpdates() {
    // Check every 2 seconds until timer is running
    checkTimerInterval = setInterval(checkIfTimerStarted, 2000);
}

function attachClickHandlers() {
        $('.tile-btn').off('click').on('click', function () {
            const tile = $(this).data('tile');
            const form = $('#game-form');
            const url = form.attr('action');  // dynamic: /play_easy, /play_normal, etc.

            $.ajax({
                type: 'POST',
                url: url,
                data: {
                    tile: tile,
                },
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                },
                success: function (data) {
                    if (data.solved) {
                        clearInterval(timerInterval);
                        window.location.href = "/result";
                        return;
                    }

                    $('#timer').text(data.elapsed_time);
                    $('#tiles-moved').text(data.tiles_moved);

                    let boardHTML = '';
                    data.board.forEach(tile => {
                        if (tile !== 0) {
                            boardHTML += `<button type="button" class="grid-item tile-btn" data-tile="${tile}">${tile}</button>`;
                        } else {
                            boardHTML += `<div class="grid-item empty"></div>`;
                        }
                    });
                    $('#board').html(boardHTML);
                    attachClickHandlers(); // reattach after DOM update
                }
            });
        });
    }