# Readers-Writers Problem using Semaphores
# Run: python readers_writers_semaphore.py
# This program creates readers_writers_beginner_simulation.html from real thread events and opens it automatically.

import json
import random
import threading
import time
import webbrowser
import os

# You can change these values.
NUMBER_OF_READERS = 4
NUMBER_OF_WRITERS = 2
READS_PER_READER = 2
WRITES_PER_WRITER = 2

shared_data = 0
reader_count = 0

# Semaphores used to control access.
reader_count_lock = threading.Semaphore(1)  # Protects reader_count
resource = threading.Semaphore(1)           # Protects shared_data
service_queue = threading.Semaphore(1)      # Helps prevent writer starvation

# A lock protects the event history and display states.
state_lock = threading.Lock()
active_readers = 0

reader_states = {f"R{i}": "Not started" for i in range(1, NUMBER_OF_READERS + 1)}
writer_states = {f"W{i}": "Not started" for i in range(1, NUMBER_OF_WRITERS + 1)}
events = []


def record_event(message):
    """Save the message and a snapshot of the current program state."""
    with state_lock:
        if any(state == "Writing" for state in writer_states.values()):
            status = "Writer is using the resource"
        elif active_readers > 0:
            status = "Readers are using the resource"
        else:
            status = "Resource is free"

        events.append({
            "message": message,
            "reader_count": active_readers,
            "shared_data": shared_data,
            "resource_status": status,
            "readers": dict(reader_states),
            "writers": dict(writer_states),
        })


def set_reader_state(reader_id, state, message):
    with state_lock:
        reader_states[reader_id] = state
        if any(s == "Writing" for s in writer_states.values()):
            status = "Writer is using the resource"
        elif active_readers > 0:
            status = "Readers are using the resource"
        else:
            status = "Resource is free"
        events.append({
            "message": message, "reader_count": active_readers,
            "shared_data": shared_data, "resource_status": status,
            "readers": dict(reader_states), "writers": dict(writer_states)
        })


def set_writer_state(writer_id, state, message):
    with state_lock:
        writer_states[writer_id] = state
        if any(s == "Writing" for s in writer_states.values()):
            status = "Writer is using the resource"
        elif active_readers > 0:
            status = "Readers are using the resource"
        else:
            status = "Resource is free"
        events.append({
            "message": message, "reader_count": active_readers,
            "shared_data": shared_data, "resource_status": status,
            "readers": dict(reader_states), "writers": dict(writer_states)
        })


def reader(number):
    """Readers can read together, but not while a writer is writing."""
    global reader_count, active_readers
    reader_id = f"R{number}"

    for _ in range(READS_PER_READER):
        set_reader_state(reader_id, "Waiting", f"{reader_id} is waiting to read.")

        # Pass through the queue. A writer can hold the queue while writing.
        service_queue.acquire()
        service_queue.release()

        reader_count_lock.acquire()
        reader_count += 1

        # The first reader locks the resource to keep writers out.
        if reader_count == 1:
            set_reader_state(reader_id, "Waiting for resource",
                             f"{reader_id} is the first reader and is requesting the resource.")
            resource.acquire()

        with state_lock:
            active_readers += 1
            reader_states[reader_id] = "Reading"
            events.append({
                "message": f"{reader_id} entered the critical section to read shared_data = {shared_data}.",
                "reader_count": active_readers, "shared_data": shared_data,
                "resource_status": "Readers are using the resource",
                "readers": dict(reader_states), "writers": dict(writer_states)
            })
        reader_count_lock.release()

        time.sleep(random.uniform(0.15, 0.4))  # Simulate reading

        reader_count_lock.acquire()
        reader_count -= 1
        with state_lock:
            active_readers -= 1
            reader_states[reader_id] = "Finished reading"
            status = "Readers are using the resource" if active_readers else "Resource is free"
            events.append({
                "message": f"{reader_id} left the reading critical section.",
                "reader_count": active_readers, "shared_data": shared_data,
                "resource_status": status,
                "readers": dict(reader_states), "writers": dict(writer_states)
            })

        # The last reader releases the resource so a writer can use it.
        if reader_count == 0:
            resource.release()
            record_event("The last reader left. The resource is available.")
        reader_count_lock.release()
        time.sleep(random.uniform(0.05, 0.15))

    set_reader_state(reader_id, "Done", f"{reader_id} completed all reads.")


def writer(number):
    """A writer gets exclusive access while changing the shared data."""
    global shared_data
    writer_id = f"W{number}"

    for _ in range(WRITES_PER_WRITER):
        set_writer_state(writer_id, "Waiting", f"{writer_id} is waiting to write.")

        # Hold the queue so new readers cannot pass while this writer waits.
        service_queue.acquire()
        resource.acquire()

        set_writer_state(writer_id, "Writing", f"{writer_id} entered the writing critical section.")

        with state_lock:
            shared_data += 1
            events.append({
                "message": f"{writer_id} updated shared_data to {shared_data}.",
                "reader_count": active_readers, "shared_data": shared_data,
                "resource_status": "Writer is using the resource",
                "readers": dict(reader_states), "writers": dict(writer_states)
            })

        time.sleep(random.uniform(0.2, 0.45))  # Simulate writing
        set_writer_state(writer_id, "Finished writing", f"{writer_id} left the writing critical section.")

        resource.release()
        service_queue.release()
        time.sleep(random.uniform(0.05, 0.15))

    set_writer_state(writer_id, "Done", f"{writer_id} completed all writes.")


def create_html():
    """Generate the HTML visualization using the recorded events."""
    event_json = json.dumps(events)
    html = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Readers-Writers Semaphore Simulation</title>
<style>
body{font-family:Arial,sans-serif;max-width:1050px;margin:24px auto;padding:0 16px;background:#f4f6fa;color:#20283a}
h1{margin-bottom:6px}.note{color:#596579}.panel{background:white;border:1px solid #dce2eb;border-radius:12px;padding:16px;margin:14px 0}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px}
.person{background:#eef2f8;border-radius:8px;padding:9px;margin:6px 0}
button{border:0;border-radius:7px;padding:9px 14px;margin:4px;background:#244b8f;color:white;cursor:pointer}
#message{font-size:1.08rem;min-height:48px}.bar{height:8px;background:#e2e7ef;border-radius:5px;overflow:hidden}.fill{height:100%;background:#3978c8;width:0}
table{width:100%;border-collapse:collapse}th,td{text-align:left;padding:8px;border-bottom:1px solid #e4e8ef}
.scroll{overflow-x:auto}.small{font-size:.9rem;color:#596579}
</style>
</head>
<body>
<h1>Readers-Writers Problem</h1>
<p class="note">Semaphore solution. This timeline comes from events recorded during real Python thread execution.</p>
<div class="panel cards">
 <div><b>Shared data</b><h2 id="data">0</h2></div>
 <div><b>Readers currently reading</b><h2 id="count">0</h2></div>
 <div><b>Shared-resource status</b><h2 id="resource">Resource is free</h2></div>
</div>
<div class="panel"><h2>Reader and writer states</h2><div class="cards">
 <div><h3>Readers</h3><div id="readers"></div></div>
 <div><h3>Writers</h3><div id="writers"></div></div>
</div></div>
<div class="panel"><h2>Event playback</h2><div id="message"></div>
 <div class="bar"><div class="fill" id="fill"></div></div><p class="small" id="position"></p>
 <button onclick="previousEvent()">Previous</button><button id="playButton" onclick="togglePlay()">Play</button><button onclick="nextEvent()">Next</button><button onclick="resetEvents()">Reset</button>
</div>
<div class="panel"><h2>Full event timeline</h2><p class="small">Click a row to inspect that recorded state.</p>
<div class="scroll"><table><thead><tr><th>#</th><th>Event</th><th>Active readers</th><th>Shared data</th><th>Resource status</th></tr></thead><tbody id="timeline"></tbody></table></div>
</div>
<script>
const events = __EVENTS__;
let current = 0, timer = null;
function showEvent(i) {
 current = Math.max(0, Math.min(i, events.length - 1));
 const e = events[current];
 document.getElementById('data').textContent = e.shared_data;
 document.getElementById('count').textContent = e.reader_count;
 document.getElementById('resource').textContent = e.resource_status;
 document.getElementById('message').textContent = e.message;
 document.getElementById('position').textContent = `Event ${current+1} of ${events.length}`;
 document.getElementById('fill').style.width = `${(current+1)/events.length*100}%`;
 document.getElementById('readers').innerHTML = Object.entries(e.readers).map(([id,s])=>`<div class="person"><b>${id}</b> — ${s}</div>`).join('');
 document.getElementById('writers').innerHTML = Object.entries(e.writers).map(([id,s])=>`<div class="person"><b>${id}</b> — ${s}</div>`).join('');
 document.querySelectorAll('#timeline tr').forEach((r,n)=>r.style.background=n===current?'#e6efff':'');
}
function nextEvent(){if(current<events.length-1)showEvent(current+1);else stopPlay();}
function previousEvent(){stopPlay();showEvent(current-1);}
function resetEvents(){stopPlay();showEvent(0);}
function togglePlay(){
 if(timer){stopPlay();return;}
 document.getElementById('playButton').textContent='Pause';
 timer=setInterval(()=>{if(current>=events.length-1){stopPlay();return;}showEvent(current+1);},900);
}
function stopPlay(){if(timer)clearInterval(timer);timer=null;document.getElementById('playButton').textContent='Play';}
events.forEach((e,i)=>{
 const row=document.createElement('tr');
 row.innerHTML=`<td>${i+1}</td><td></td><td>${e.reader_count}</td><td>${e.shared_data}</td><td></td>`;
 row.children[1].textContent=e.message;row.children[4].textContent=e.resource_status;
 row.style.cursor='pointer';row.onclick=()=>{stopPlay();showEvent(i);};
 document.getElementById('timeline').appendChild(row);
});
showEvent(0);
</script></body></html>"""
    html = html.replace("__EVENTS__", event_json)
    filename = "readers_writers_beginner_simulation.html"
    with open(filename, "w", encoding="utf-8") as file:
        file.write(html)
    
    # Automatically open the generated HTML file in the default web browser
    file_path = os.path.abspath(filename)
    webbrowser.open(f"file://{file_path}")


def main():
    record_event("Simulation started. Shared data starts at 0.")

    threads = []
    for number in range(1, NUMBER_OF_READERS + 1):
        threads.append(threading.Thread(target=reader, args=(number,)))
    for number in range(1, NUMBER_OF_WRITERS + 1):
        threads.append(threading.Thread(target=writer, args=(number,)))

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    record_event("Simulation finished. All threads completed.")
    create_html()

    print("Readers-Writers simulation completed.")
    print(f"Readers: {NUMBER_OF_READERS}; writers: {NUMBER_OF_WRITERS}")
    print(f"Read operations: {NUMBER_OF_READERS * READS_PER_READER}")
    print(f"Write operations: {NUMBER_OF_WRITERS * WRITES_PER_WRITER}")
    print(f"Events recorded: {len(events)}")
    print("HTML file created and opened in browser: readers_writers_beginner_simulation.html")


if __name__ == "__main__":
    main()
