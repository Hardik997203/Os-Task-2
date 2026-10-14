Operating Systems Programming Assignment
AI-Assisted Synchronization and Visualization
1. Student Information
•	Student Name: Hardik Shetty
•	USN: NNM24IS090
2. Project Description
This project demonstrates thread synchronization in Operating Systems through the Readers-Writers Problem and the Dining Philosophers Problem. Python threads and synchronization mechanisms are used to coordinate access to shared resources.
The submitted programs also record execution events and generate HTML visualizations to help understand the sequence of states during execution.
1.	Readers-Writers Problem using Semaphores.
2.	Dining Philosophers Problem using Monitor-Style Synchronization.
3. Programming Language and Libraries
Programming language: Python 3
Libraries used:
•	threading — creates threads and provides synchronization mechanisms.
•	time — introduces delays and records elapsed time.
•	random — generates variable delays to simulate concurrent execution.
•	json — converts recorded events into data that can be embedded in HTML.
•	webbrowser — opens the generated HTML visualization.
•	os — handles file paths.
•	html — imported by the Dining Philosophers program.
Visualization technologies:
•	HTML for the web page structure.
•	CSS for styling.
•	JavaScript for event playback and interactive visualization.
•	A modern web browser for viewing the generated HTML files.
All imported Python modules are part of the Python standard library. No additional Python packages are required.
4.  Build and Compilation Instructions
Tools required:
•	Python 3
•	Visual Studio Code (VS Code)
Steps:
1.	Install Python 3 and Visual Studio Code.
2.	Open the project folder in VS Code.
3.	Make sure the Python extension is installed in VS Code.
4.	Open the required Python file.
5.	Run the program using the Run Python File button or the VS Code terminal.
No separate compilation step is required because Python is an interpreted language.

5. Implementation 1: Readers-Writers Using Semaphores
Python file: Readerwriters (3).py
Objective
The objective is to coordinate multiple readers and writers accessing shared data while maintaining mutual exclusion between readers and writers.
Program details
•	Creates four reader threads and two writer threads.
•	Each reader performs two read operations.
•	Each writer performs two write operations.
•	Multiple readers can read the shared data simultaneously.
•	A writer requires exclusive access to the shared resource while writing.
Synchronization mechanisms
•	reader_count_lock protects the reader count.
•	resource controls access to the shared resource.
•	service_queue helps prevent new readers from repeatedly bypassing a waiting writer.
•	state_lock protects the event history and display-state information.
The first reader acquires the shared resource, preventing writers from entering while readers are active. The last reader releases the resource. Writers acquire the resource before updating the shared data.
HTML simulation
The program generates:
readers_writers_beginner_simulation.html
The HTML visualization displays:
•	Shared data value.
•	Number of active readers.
•	Current resource status.
•	Reader and writer states.
•	Recorded execution events.
•	Interactive event playback controls.
The event playback supports Previous, Play/Pause, Next, and Reset operations. Selecting a row in the event timeline allows the corresponding recorded state to be viewed.
6. Implementation 2: Dining Philosophers Using Monitor-Style Synchronization
Python file: Dining_philo_monitors (3).py
Objective
The objective is to coordinate four philosophers sharing four forks while preventing conflicting fork ownership.
Program details
•	Creates exactly four philosopher threads and four forks.
•	Each philosopher attempts to eat three meals.
•	Each philosopher moves through states such as Thinking, Hungry/Waiting, Acquiring Forks, Eating, and Releasing Forks.
•	Both required forks must be available before a philosopher acquires them.
Synchronization mechanisms
•	threading. Lock protects shared synchronization data.
•	threading. Condition allows philosophers to wait for the required conditions and be notified when forks become available.
•	waiting_queue maintains the FIFO order of waiting philosophers.
•	fork_owner records the owner of each fork.
•	state records each philosopher's current state.
A philosopher must be at the front of the waiting queue and both required forks must be available. Both forks are assigned together inside the protected section. After eating, the philosopher releases both forks and notifies waiting philosophers.
HTML simulation
The program generates:
dining_philosophers.html
The HTML visualization displays:
•	The current state of each philosopher.
•	Availability and ownership of the four forks.
•	The FIFO waiting queue.
•	Recorded execution events and elapsed time.
•	An event timeline with a slider.
•	Previous, Play/Pause, Next, and Reset controls.
The visualization uses events recorded during the Python program's execution.
7. Execution Instructions
Run Both programs can be executed separately using Visual Studio Code.
Run the Readers-Writers Program
1.	Open Visual Studio Code.
2.	Open the folder containing Readerwriters (3).py.
3.	Open the Python file.
4.	Click the Run Python File button in the top-right corner, or right-click inside the editor and select Run Python File in Terminal.
5.	Wait for the simulation to finish. The program generates readers_writers_beginner_simulation.html and attempts to open it in your default browser.
Run the Dining Philosophers Program
1.	Open Visual Studio Code.
2.	Open the folder containing Dining_philo_monitors (3).py.
3.	Open the Python file.
4.	Click the Run Python File button in the top-right corner, or right-click inside the editor and select Run Python File in Terminal.
5.	Wait for all philosopher threads to finish. The program generates dining_philosophers.html and attempts to open it in your default browser.

8. Generating the HTML Simulations
The HTML files are generated automatically by the Python programs after the threads finish executing.
Readers-Writers
1.	Run Readerwriters (3).py.
2.	Wait for the threads to complete.
3.	The program records the final event and creates readers_writers_beginner_simulation.html.
4.	The program attempts to open the generated HTML file in the default browser.
Dining Philosophers
1.	Run Dining_philo_monitors (3).py.
2.	Wait for all four philosopher threads to finish their meals.
3.	The program creates dining_philosophers.html.
4.	The program attempts to open the generated HTML file in the default browser.
The HTML files are created in the program's current working directory. Run the programs from the folder where you want the files to be created.
9. Opening and Viewing the HTML Files
If a generated HTML file does not open automatically:
1.	Open the folder in which you ran the Python program.
2.	Find the corresponding HTML file.
3.	Double-click the file to open it in a web browser.
4.	Use the available playback controls to inspect the recorded execution.
For the Readers-Writers visualization, review the reader and writer states, shared data, resource status, and event timeline.
For the Dining Philosophers visualization, review philosopher states, fork ownership, the FIFO waiting queue, and the event log.
The HTML files can be viewed locally and do not require a web server.
10. Expected Output and Sample Screenshots
Readers-Writers expected output
The terminal displays a completion message, the number of readers and writers, the total number of read and write operations, the number of recorded events, and the generated HTML filename.
The HTML page displays the shared data, active reader count, resource status, reader and writer states, and event playback timeline.
Dining Philosophers expected output
The terminal displays a completion message, the number of recorded execution events, and the generated HTML filename.
The HTML page displays the four philosophers, four forks, fork ownership, the waiting queue, and the recorded event sequence.
The precise event order can vary between runs because thread scheduling and simulated delays are variable.
Sample screenshots
Add screenshots of your actual program output to the repository. Suggested files are:
•	screenshots/readers_writers_terminal.png — terminal output after the Readers-Writers program finishes.
•	screenshots/readers_writers_html.png — Readers-Writers HTML simulation.
•	screenshots/dining_philosophers_terminal.png — terminal output after the Dining Philosophers program finishes.
•	screenshots/dining_philosophers_html.png — Dining Philosophers HTML simulation.
Create a screenshots folder and save your screenshots using these filenames, or update the names below to match your actual files.
Readers-Writer’s screenshot






Dining Philosophers screenshot





.
11. Known Limitations
•	The execution order may differ between runs because the operating system schedules threads concurrently.
•	The Readers-Writers program uses a service queue to help prevent writer starvation, but it does not guarantee strict FIFO fairness.
•	The Dining Philosophers program uses a FIFO waiting queue, but starvation freedom is not formally guaranteed under every possible execution.
•	The HTML visualizations display recorded execution events; they do not perform the synchronization themselves.
•	A browser is required to view the generated HTML files.
•	The two documented programs cover only two of the four implementations required by the assignment. The Readers-Writers monitor-based implementation and Dining Philosophers semaphore-based implementation must be added separately to complete all four variants.
12. AI Tools Used and Prompt Log
The AI tools used during the project include:
•	ChatGPT — assistance with understanding synchronization concepts, reviewing code, explaining program behavior, and preparing documentation.
•	Kimi — AI assistance used during the project for generating code
•	Gemini — AI assistance used during the project for understanding to code and generating code
Prompt log
Prompt log link: 
https://share.gemini.google/88k4sYHtH0LB
https://chatgpt.com/s/p_6acfab63bfbc8191ac9166d4869d8c3d


13. References
1.	B. Ge-Li, “A SOLUTION FOR THE DEADLOCK OF DINING PHILOSOPHERS,” Journal of Inner Mongolia Agricultural University, Jan. 2010.
2.	Python Software Foundation. threading — Thread-based Parallelism. https://docs.python.org/3/library/threading.html
3.	Python Software Foundation. json — JSON Encoder and Decoder. https://docs.python.org/3/library/json.html
4.	Operating Systems Programming Assignment instructions provided for this project.
14. Acknowledgements
I acknowledge the use of ChatGPT, Kimi, and Gemini as AI assistance tools during the development and documentation of this project.
The purpose of the project is to demonstrate synchronization concepts, thread coordination, shared-resource access, event recording, and visualization of execution states.
The submitted source code and actual execution results should be used as the basis for explaining the implementation.

