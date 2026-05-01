$(document).ready(function() {
    var selected_difficulty = $("input[name=difficulty]:checked").val();
    showTimeLeaderboard(selected_difficulty);

    $("input[name=difficulty]").on("change", function() {
        selected_difficulty = $("input[name=difficulty]:checked").val();
        showTimeLeaderboard(selected_difficulty);
    });
});

function showTimeLeaderboard(selected_difficulty) {
var time = `<h3 id="time" class="text-light py-2">Time</h3>
            <div class="row leaderboard-input">
                <div class="col">
                    <p class="text-light fs-6">Rank</p>
                </div>
                <div class="col">
                    <p class="text-light fs-6">Username</p>
                </div>
                <div class="col">
                    <p class="text-light fs-6">Time</p>
                </div>
                <div class="col">
                    <p class="text-light fs-6">Tiles Moved</p>
                </div>
            </div>`
var tile = `<h3 id="tiles_moved" class="text-light py-2">Tiles Moved</h3>
            <div class="row leaderboard-input">
                <div class="col">
                    <p class="text-light fs-6">Rank</p>
                </div>
                <div class="col">
                    <p class="text-light fs-6">Username</p>
                </div>
                <div class="col">
                    <p class="text-light fs-6">Tiles Moved</p>
                </div>
                <div class="col">
                    <p class="text-light fs-6">Time</p>
                </div>
            </div>`

        $.post("/fetch_score", {mode: selected_difficulty}, function(data) {
            for (let i = 0; i < data.time_leaderboard.length; i++) {
                time += `<div class="row leaderboard-input border-top">
                    <div class="col">
                        <p class="text-light fs-5">${i+1}</p>
                    </div>
                    <div class="col">
                        <p class="text-light fs-5">${data.time_leaderboard[i][1]}</p>
                    </div>
                    <div class="col">
                        <p class="text-light fs-5">${data.time_leaderboard[i][2]}s</p>
                    </div>
                    <div class="col">
                        <p class="text-light fs-5">${data.time_leaderboard[i][3]}</p>
                    </div>
                </div>`;

                tile += `<div class="row leaderboard-input border-top">
                    <div class="col">
                        <p class="text-light fs-5">${i+1}</p>
                    </div>
                    <div class="col">
                        <p class="text-light fs-5">${data.tiles_moved_leaderboard[i][1]}</p>
                    </div>
                    <div class="col">
                        <p class="text-light fs-5">${data.tiles_moved_leaderboard[i][3]}</p>
                    </div>
                    <div class="col">
                        <p class="text-light fs-5">${data.tiles_moved_leaderboard[i][2]}s</p>
                    </div>
                </div>`;
            }

            $("#time-leaderboard").html(time);
            $("#tile-leaderboard").html(tile);

            if (selected_difficulty == "easy") {
            $("#leaderboard-bg").removeClass("bg-warning");
            $("#leaderboard-bg").removeClass("bg-danger");

            $("#leaderboard-bg").addClass("bg-success");
            $("h3").addClass("text-light");
            $(".leaderboard-input .col p").addClass("text-light");
            $("#time-leaderboard").removeClass("border-dark");
            $("#tile-leaderboard").removeClass("border-dark");
        }
        else if (selected_difficulty == "normal") {
            $("#leaderboard-bg").removeClass("bg-success");
            $("#leaderboard-bg").removeClass("bg-danger");
            $("#leaderboard-bg").addClass("bg-warning");
            $("h3").removeClass("text-light");
            $(".leaderboard-input .col p").removeClass("text-light");
            $("#time-leaderboard").addClass("border-dark");
            $("#tile-leaderboard").addClass("border-dark");
            $(".leaderboard-input").addClass("border-dark");
        }
        else {
            $("#leaderboard-bg").removeClass("bg-success");
            $("#leaderboard-bg").removeClass("bg-warning");
            $("#leaderboard-bg").addClass("bg-danger");
            $("h3").addClass("text-light");
            $(".leaderboard-input .col p").addClass("text-light");
            $("#time-leaderboard").removeClass("border-dark");
            $("#tile-leaderboard").removeClass("border-dark");
        }
        });
}