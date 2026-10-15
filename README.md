# OS Synchronization Assignment - Readers-Writers & Dining Philosophers

**Student Name:** Hardik Shetty  
**USN:** NNM24IS090
**Course:** Operating Systems  

---

## 1. Project Overview
This repository contains two standalone synchronization implementations demonstrating classical concurrency problems using Python threads and synchronization primitives. The Readers-Writers program uses semaphores and a service queue to coordinate readers and writers, while the Dining Philosophers program uses a monitor with a lock, condition variable, and FIFO waiting queue to coordinate four philosophers. Both programs record runtime state transitions and generate self-contained, browser-viewable HTML simulations from the recorded execution events.

| # | Problem | Technique | Source File | Generated HTML |
|---|---|---|---|---|
| 1 | Readers-Writers | Semaphores (`reader_count_lock`, `resource`, `service_queue`), service queue to help prevent writer starvation | `Readerwriters(4).py` | `readers_writers_beginner_simulation.html` |
| 2 | Dining Philosophers (4) | Monitor (`Lock` + `Condition` variable), FIFO waiting queue, atomic fork allocation | `Dining_philo_monitors(4).py` | `dining_philosophers.html` |

---

## 2. Language and Environment Requirements
- **Language:** Python 3.8 or later
- **Dependencies:** Python Standard Library only (`threading`, `time`, `json`, `random`, `webbrowser`, `os`, and `html` where used). No third-party packages or virtual environments are required.
- **Browser:** Any modern web browser, such as Chrome, Edge, Firefox, or Safari.

---

## 3. Build / Compilation Instructions
Python is an interpreted language; no compilation or build step is required.

---

## 4. Execution & HTML Generation
Run each program directly from the command prompt or terminal using Python. Make sure you are in the folder containing the Python files.

**Run the Readers-Writers program**

```bash
python "Readerwriters(4).py"
```

Alternatively, on systems that use Python 3:

```bash
python3 "Readerwriters(4).py"
```

**Run the Dining Philosophers program**

```bash
python "Dining_philo_monitors(4).py"
```

Alternatively:

```bash
python3 "Dining_philo_monitors(4).py"
```

After execution, the programs generate their respective HTML simulation files.

- **Readers-Writers:** Creates `readers_writers_beginner_simulation.html` and automatically attempts to open it in the default web browser.
- **Dining Philosophers:** Creates `dining_philosophers.html` and automatically attempts to open it in the default web browser.

If the HTML file does not open automatically, open the generated file manually in a web browser.

The Readers-Writers simulation displays reader and writer states, shared data, resource status, and an event timeline with playback controls.

The Dining Philosophers simulation displays the states of four philosophers, fork ownership, the FIFO waiting queue, and an execution log with replay controls.

Both HTML simulations are generated from events recorded during the Python programs' actual thread execution.
