
import threading
import time
import json
import html
import random
import webbrowser
import os
# Exactly four philosophers and four forks
N = 4
MEALS_EACH = 3

# Philosopher states
THINKING = "Thinking"
HUNGRY = "Hungry/Waiting"
ACQUIRING = "Acquiring Forks"
EATING = "Eating"
RELEASING = "Releasing Forks"

# Shared monitor lock and condition variable
lock = threading.Lock()
condition = threading.Condition(lock)

# Shared data
state = [THINKING] * N
fork_owner = [None] * N
waiting_queue = []

# Execution events used to generate the HTML file
events = []
event_number = 0


def record_event(message):
    """Record the real state of the program for the HTML file."""
    global event_number

    event_number += 1

    events.append({
        "number": event_number,
        "message": message,
        "states": state.copy(),
        "forks": fork_owner.copy(),
        "queue": waiting_queue.copy(),
        "time": round(time.monotonic() - start_time, 2)
    })


def left_fork(p):
    return p


def right_fork(p):
    return (p + 1) % N


def philosopher(p):
    """Each philosopher thinks, waits, eats and releases forks."""

    for meal in range(1, MEALS_EACH + 1):

        # Thinking
        with condition:
            state[p] = THINKING
            record_event(f"P{p} is thinking")
        time.sleep(random.uniform(0.2, 0.6))

        # Enter the FIFO waiting queue
        with condition:
            state[p] = HUNGRY
            waiting_queue.append(p)
            record_event(f"P{p} joined the FIFO queue")
            condition.notify_all()

            # Wait until this philosopher is first in the queue
            # and both required forks are available.
            while (
                waiting_queue[0] != p
                or fork_owner[left_fork(p)] is not None
                or fork_owner[right_fork(p)] is not None
            ):
                condition.wait()

            # Acquiring Forks
            state[p] = ACQUIRING
            record_event(f"P{p} is acquiring both forks")

            # Both forks are assigned together inside the monitor.
            fork_owner[left_fork(p)] = p
            fork_owner[right_fork(p)] = p

            waiting_queue.pop(0)
            record_event(f"P{p} acquired F{left_fork(p)} and F{right_fork(p)}")

            # Eating
            state[p] = EATING
            record_event(f"P{p} started eating meal {meal}")

        # Eating happens outside the monitor lock.
        # Other philosophers can use their available forks.
        time.sleep(random.uniform(0.3, 0.7))

        # Release both forks
        with condition:
            state[p] = RELEASING
            record_event(f"P{p} is releasing forks")

            fork_owner[left_fork(p)] = None
            fork_owner[right_fork(p)] = None
            record_event(f"P{p} released both forks")

            # Wake waiting philosophers to check the queue.
            condition.notify_all()

    # All meals completed
    with condition:
        state[p] = THINKING
        record_event(f"P{p} finished all {MEALS_EACH} meals")


def generate_html():
    """Create an HTML visualization from recorded execution events."""

    event_data = json.dumps(events).replace("</", "<\\/")

    page = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Dining Philosophers - Monitor and FIFO</title>
<style>
body {
    font-family: Arial, sans-serif;
    margin: 20px auto;
    padding: 0 16px;
    max-width: 1050px;
    background: #f3f6fa;
    color: #172033;
}
h1, h2 { text-align: center; }
.subtitle { text-align: center; color: #526078; }
.panel {
    background: white;
    border-radius: 12px;
    padding: 18px;
    margin: 16px 0;
    box-shadow: 0 2px 8px #00000012;
}
.seats {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 12px;
}
.philosopher {
    padding: 14px;
    border-radius: 9px;
    border: 2px solid #dce3ed;
}
.state {
    font-weight: bold;
    margin-top: 8px;
}
.forks {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 8px;
}
.fork {
    background: #e8eef7;
    border-radius: 8px;
    padding: 12px 5px;
    text-align: center;
    overflow-wrap: anywhere;
}
.free { background: #d9f7e8; }
.busy { background: #ffe6bd; }
.controls {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    align-items: center;
}
button {
    padding: 9px 14px;
    border: 0;
    border-radius: 7px;
    cursor: pointer;
    background: #2458a6;
    color: white;
}
input[type=range] { flex: 1; min-width: 150px; }
#log {
    max-height: 320px;
    overflow-y: auto;
}
.log-row {
    padding: 8px;
    border-bottom: 1px solid #e5eaf1;
    font-size: 14px;
}
.active {
    background: #e1edff;
    font-weight: bold;
}
.note { color: #526078; font-size: 14px; }
@media(max-width: 600px) {
    .seats { grid-template-columns: 1fr; }
    .forks { grid-template-columns: repeat(2, 1fr); }
}
</style>
</head>
<body>
<h1>Dining Philosophers Problem</h1>
<p class="subtitle">Monitor + Condition Variable + FIFO Queue</p>

<div class="panel">
    <h2>Execution Replay</h2>
    <div class="controls">
        <button onclick="previousEvent()">Previous</button>
        <button id="play" onclick="togglePlay()">Play</button>
        <button onclick="nextEvent()">Next</button>
        <button onclick="resetReplay()">Reset</button>
    </div>
    <p id="progress"></p>
    <input id="timeline" type="range" min="0" value="0"
           step="1" oninput="showEvent(Number(this.value))">
    <p id="message"></p>
    <p class="note">This replay uses the execution events recorded by the
    Python synchronization program, not a separate simulated schedule.</p>
</div>

<div class="panel">
    <h2>Philosopher States</h2>
    <div id="philosophers" class="seats"></div>
</div>

<div class="panel">
    <h2>Four Forks</h2>
    <div id="forks" class="forks"></div>
</div>

<div class="panel">
    <h2>FIFO Waiting Queue</h2>
    <p id="queue"></p>
</div>

<div class="panel">
    <h2>Execution Log</h2>
    <div id="log"></div>
</div>

<script>
const events = EVENT_DATA;
let current = 0;
let timer = null;

const colors = {
    "Thinking": "#e8eef7",
    "Hungry/Waiting": "#fff0b8",
    "Acquiring Forks": "#dce5ff",
    "Eating": "#c9f5d9",
    "Releasing Forks": "#ffdcd5"
};

function showEvent(index) {
    current = Math.max(0, Math.min(index, events.length - 1));
    const e = events[current];

    document.getElementById("timeline").max = events.length - 1;
    document.getElementById("timeline").value = current;
    document.getElementById("progress").textContent =
        "Event " + (current + 1) + " of " + events.length +
        " | Time: " + e.time + " seconds";
    document.getElementById("message").textContent = e.message;

    document.getElementById("philosophers").innerHTML =
        e.states.map((s, p) =>
            '<div class="philosopher" style="background:' +
            colors[s] + '">' +
            '<strong>Philosopher P' + p + '</strong>' +
            '<div class="state">' + s + '</div>' +
            '<div>Left fork: F' + p + '</div>' +
            '<div>Right fork: F' + ((p + 1) % 4) + '</div>' +
            '</div>'
        ).join("");

    document.getElementById("forks").innerHTML =
        e.forks.map((owner, f) =>
            '<div class="fork ' + (owner === null ? "free" : "busy") +
            '"><strong>Fork F' + f + '</strong><br>' +
            (owner === null ? "Available" : "Owned by P" + owner) +
            '</div>'
        ).join("");

    document.getElementById("queue").textContent =
        e.queue.length ? e.queue.map(p => "P" + p).join(" → ")
                       : "Empty — no philosophers waiting";

    document.getElementById("log").innerHTML =
        events.slice(0, current + 1).map((item, i) =>
            '<div class="log-row ' + (i === current ? "active" : "") +
            '">#' + item.number + ' (' + item.time + 's): ' +
            escapeText(item.message) + '</div>'
        ).join("");

    const log = document.getElementById("log");
    log.scrollTop = log.scrollHeight;
}

function escapeText(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
}

function previousEvent() { pause(); showEvent(current - 1); }
function nextEvent() { pause(); showEvent(current + 1); }
function resetReplay() { pause(); showEvent(0); }

function pause() {
    if (timer !== null) {
        clearInterval(timer);
        timer = null;
    }
    document.getElementById("play").textContent = "Play";
}

function togglePlay() {
    if (timer !== null) {
        pause();
        return;
    }

    if (current >= events.length - 1) showEvent(0);

    document.getElementById("play").textContent = "Pause";
    timer = setInterval(() => {
        if (current >= events.length - 1) {
            pause();
        } else {
            showEvent(current + 1);
        }
    }, 500);
}

showEvent(0);
</script>
</body>
</html>"""

    page = page.replace("EVENT_DATA", event_data)

    with open("dining_philosophers.html", "w", encoding="utf-8") as file:
        file.write(page)


if __name__ == "__main__":
    start_time = time.monotonic()

    # Initial snapshot
    with condition:
        record_event("Simulation started")

    # Start exactly four philosopher threads
    threads = []

    for p in range(N):
        t = threading.Thread(target=philosopher, args=(p,))
        threads.append(t)
        t.start()

    # Wait for every philosopher to finish
    for t in threads:
        t.join()

    # Save the HTML using the real recorded execution events
    generate_html()

    print("Simulation completed.")
    print("Total execution events:", len(events))
    print("HTML file created: dining_philosophers.html")
    # Generate the HTML file
generate_html()

print("Simulation completed.")
print("Total execution events:", len(events))
print("HTML file created: dining_philosophers.html")

# Open the HTML file automatically in the browser
html_path = os.path.abspath("dining_philosophers.html")
webbrowser.open("file:///" + html_path.replace("\\", "/"))
