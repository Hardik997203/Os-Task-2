# AI Usage Documentation

**Student Name:** Hardik (NNM24IS090)  
**Course:** Operating Systems

---

## 1 AI Tools Used

The following AI tools were used as assistance while working on this Operating Systems synchronization assignment:

1. **ChatGPT (OpenAI):** Used to understand the Readers-Writers and Dining Philosophers problems from the basics, understand synchronization concepts, prepare project documentation, and explain the code in a simple way.

2. **Kimi:** Used as an AI-assisted tool for generating code for the synchronization problems.

3. **Google Gemini:** Used as an AI-assisted tool for understanding operating system concepts, preparing the assignment report, and improving the project documentation.

---

## 2 Initial Prompts Used

The following prompts represent the types of questions used to understand and develop the project:

➢ "I am a beginner learning about the Readers-Writers and Dining Philosophers problems. Help me understand these concepts from the basics."

➢ "Explain the structure and working of the Readers-Writers problem using Python threads and semaphores in a simple way."

➢ "Help me understand the use of semaphores, including `reader_count_lock`, `resource`, and `service_queue`, in my Readers-Writers program."

➢ "Explain my Dining Philosophers monitor-based program, including the lock, condition variable, fork ownership, and FIFO waiting queue."

➢ "Explain mutual exclusion, race conditions, deadlock, and starvation with reference to my actual code."

➢ "Explain how my Python programs record execution events and generate HTML simulations from the recorded events."

➢ "Help me prepare a README file and assignment report that accurately describe my submitted Python programs."

---

## 3 Manual Changes and Verification

The code was reviewed to understand how threads are synchronized, how shared resources are accessed, and how the execution states are recorded. The explanations used in the documentation were compared with the synchronization mechanisms present in the submitted programs.

In the **Readers-Writers program**, semaphores are used to coordinate reader and writer access. The `reader_count_lock` semaphore protects updates to the reader count, the `resource` semaphore controls access to the shared resource, and the `service_queue` semaphore helps prevent writers from being continuously bypassed by new readers. Multiple readers can read the shared data at the same time, while writing requires exclusive access.

In the **Dining Philosophers program**, a monitor-style approach is implemented using Python's `Lock` and `Condition` variable. Four philosopher threads share four forks. A FIFO waiting queue determines the order of requests, and a philosopher must be first in the queue and have both required forks available before acquiring them. The program records philosopher states, fork ownership, queue contents, and execution time.

Both programs record events during execution and use those events to generate HTML visualizations. The Readers-Writers simulation displays reader and writer states, shared data, resource status, and an interactive event timeline. The Dining Philosophers simulation displays philosopher states, fork ownership, the FIFO waiting queue, and an execution log with playback controls.

The project documentation was prepared to match the two submitted programs. The descriptions of synchronization, resource access, and HTML generation are based on the code rather than on unrelated implementations.

