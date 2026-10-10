# Adaptive Study Desk

An individual AI/HCI coursework prototype that learns which of two layouts works better for different study tasks. The examples are fictional; their dates and requirements are not real course instructions.

Source: <https://github.com/Jamesris1/adaptive-ai-course-portfolio/tree/main/adaptive_study_ui>

## Run the application

Use Python 3. No third-party Python packages, paid API, account, or model download is required.

1. Extract the source ZIP and open a terminal in `adaptive_study_ui`.
2. On Windows, run `python server.py`. On macOS/Linux, run `python3 server.py`.
3. Open <http://127.0.0.1:8765> in a current browser.
4. Stop the server with Ctrl+C in that terminal.

The server listens on the local computer only. Keep all seven files together and use the server rather than opening `index.html` directly. The code uses browser ES modules. If port 8765 is busy, run `python server.py --port 8766` and open that port instead. macOS compatibility has not been verified on a Mac.

## Try the adaptation

Complete the sample deadline, priority, and requirements tasks. The guided layout presents labeled assignment cards; the compact layout presents the information in a table. Both contain the same task facts.

Check **Learn from my task interactions**, then click **Start next task**. Learning starts with the next task, including when the checkbox is enabled midway through a task. In automatic mode with learning enabled, the application chooses a layout at each task's start. It first tries guided, then compact for that task context, and later compares observed rewards while continuing to explore. With learning off, automatic mode always uses guided and ignores learned estimates. Layouts do not change while a task is in progress.

The manual layout selector lets you keep a fixed view. This is an *adaptable* control: the user chooses the setting. Automatic layout selection is *adaptive*: the application changes its choice using learned interaction outcomes. Manual choices can also supply outcomes when learning is enabled.

The interface explains its choice and shows aggregate learning statistics. Clear learned data to start again. Repeat a task to collect more observations; two completions show initial exploration, not a reliable preference estimate.

## How the AI works

`learner.mjs` implements a small contextual bandit. Each context (`deadline`, `priority`, or `requirements`) has separate guided and compact estimates. After successful completion, the selected layout receives this reward:

```text
reward = clamp(1 - min(seconds / 60, 0.60)
                 - min(errors * 0.15, 0.30)
                 - min(hints * 0.05, 0.10), 0, 1)
```

`seconds` means active elapsed time while the browser tab is visible. The timer pauses when the tab is hidden. `errors` counts incorrect answer attempts; `hints` counts the first hint reveal for that task. Its count and running mean are updated online. For layouts with observations, the selection score is:

```text
mean reward + sqrt(2 * ln(total context observations) / layout observations)
```

This upper-confidence-bound (UCB) rule balances observed performance and exploration. It is learning from feedback rather than selecting a layout solely from fixed screen-width rules. There is no language model or chatbot in the running application.

The reward weights are classroom design choices. Hint use, reading speed, and task completion time are imperfect measures of user experience. The model does not infer disability, personality, or intelligence. It cannot establish that a layout improves learning, satisfaction, or accessibility.

## Data and user control

The application uses fictional task content and does not request names, accounts, personal deadlines, or assignment uploads. Learning is opt-in. Its persistent profile contains only a version number and six pairs of observation counts and mean rewards. Raw answers and interaction logs are not retained in that profile.

The profile stays in the current browser's local storage; it is not sent to an AI service. If storage is unavailable or unreadable, learning can continue in memory for the current page session. Learning is off by default on every visit, even when saved estimates exist. Those estimates are displayed but not used for automatic selection while learning is off.

**Clear learned data** removes this application's saved profile, resets its estimates, and cancels logging for the current task. Unchecking learning also cancels the current task's logging, but does not delete prior observations. View preference and task changes apply only after **Start next task**.

## Source files

| File | Purpose |
| --- | --- |
| `index.html` | Accessible application structure and controls |
| `styles.css` | Guided/compact layouts and responsive styling |
| `app.mjs` | Sample tasks, interaction handling, consent, and persistence |
| `learner.mjs` | UCB selection, rewards, updates, and profile validation |
| `server.py` | Local Python standard-library web server |
| `tests.mjs` | Model and storage-schema functional tests |
| `README.md` | Setup, behavior, limitations, and credits |

## Verification

Node.js is optional and needed only to run `node tests.mjs`. The tests check exploration, reward calculations, running means, context isolation, invalid data, and synthetic adaptation. The controlled simulation supplies different outcomes to the two layouts; it checks algorithm behavior, not benefits measured with real users.

A meaningful future evaluation would compare both layouts and automatic adaptation with consenting participants, balancing task order and measuring errors, time, accessibility, perceived control, and satisfaction. The current prototype does not claim a human usability study.

## Sources and AI assistance

Auer, P., Cesa-Bianchi, N., & Fischer, P. (2002). Finite-time analysis of the multiarmed bandit problem. *Machine Learning, 47*(2–3), 235–256. <https://doi.org/10.1023/A:1013689704352>

Sutton, R. S., & Barto, A. G. (2018). *Reinforcement learning: An introduction* (2nd ed.). MIT Press. <https://mitpress.mit.edu/9780262039246/reinforcement-learning/>

The contextual UCB implementation was written for this assignment using bandit concepts described by Sutton and Barto and the UCB1 selection rule described by Auer and colleagues. It is not a copied external example project. Python and browser standard-library/platform facilities provide the server and interface; there are no external application dependencies.

OpenAI Codex assisted with creating the interface, learning module, server, and tests, debugging, source research, and drafting the accompanying APA report. The report includes the assignment's AI-assistance disclosure. James must review and understand the code and revise any first-person account to match his own work and experience before submission.
