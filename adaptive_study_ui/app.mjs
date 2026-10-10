import { createProfile, sanitizeProfile, chooseMode, recordOutcome } from './learner.mjs';

const key = 'adaptive-study-desk-v1';
const names = { deadline: 'Find a deadline', priority: 'Choose a priority', requirements: 'Check requirements' };
const lessons = [
  { name: 'Methods note', due: 'Tuesday', priority: 'High', sources: '4' },
  { name: 'Reading reflection', due: 'Thursday', priority: 'Medium', sources: '2' },
  { name: 'Interface sketch', due: 'Friday', priority: 'Low', sources: '1' }
];
const variants = {
  deadline: [
    { question: 'When is the Methods note due?', options: ['Tuesday', 'Thursday', 'Friday'], answer: 'Tuesday', hint: 'Find Methods note, then read its due day.' },
    { question: 'When is the Interface sketch due?', options: ['Tuesday', 'Thursday', 'Friday'], answer: 'Friday', hint: 'Find Interface sketch, then read its due day.' }
  ],
  priority: [
    { question: 'Which assignment has the highest priority?', options: lessons.map(x => x.name), answer: 'Methods note', hint: 'Compare the priority labels. High comes before Medium and Low.' },
    { question: 'Which assignment has medium priority?', options: lessons.map(x => x.name), answer: 'Reading reflection', hint: 'Look for the Medium priority label.' }
  ],
  requirements: [
    { question: 'How many sources does the Methods note require?', options: ['1', '2', '4'], answer: '4', hint: 'Find Methods note and read its required sources.' },
    { question: 'How many sources does the Reading reflection require?', options: ['1', '2', '4'], answer: '2', hint: 'Find Reading reflection and read its required sources.' }
  ]
};
const $ = id => document.getElementById(id);
let profile = createProfile();
let persistent = true;
let started = false;
let task;
const sequence = { deadline: 0, priority: 0, requirements: 0 };
let taskNumber = 0;
try {
  const stored = localStorage.getItem(key);
  if (stored) profile = sanitizeProfile(JSON.parse(stored));
} catch { persistent = false; }

function storageStatus() {
  $('storage-status').textContent = persistent
    ? 'Learning is off by default each visit. Existing model statistics stay on this device until cleared.'
    : 'Browser storage is unavailable or unreadable. Learning works in memory for this visit.';
}
function persist() {
  if (!persistent) return;
  try { localStorage.setItem(key, JSON.stringify(profile)); }
  catch { persistent = false; storageStatus(); }
}
function renderStatistics() {
  $('statistics').replaceChildren(...Object.entries(names).map(([context, label]) => {
    const row = document.createElement('tr');
    const heading = document.createElement('th');
    heading.scope = 'row'; heading.textContent = label; row.append(heading);
    for (const mode of ['guided', 'compact']) {
      const cell = document.createElement('td'); const arm = profile.contexts[context][mode];
      cell.textContent = `${arm.count} completed · ${arm.count ? arm.mean.toFixed(2) : '—'} mean reward`;
      row.append(cell);
    }
    return row;
  }));
}
function renderData(mode) {
  const host = $('study-data'); host.replaceChildren();
  if (mode === 'guided') {
    const cards = document.createElement('div'); cards.className = 'cards';
    for (const lesson of lessons) {
      const card = document.createElement('article'); card.className = 'study-card';
      const heading = document.createElement('h3'); heading.textContent = lesson.name; card.append(heading);
      const list = document.createElement('dl');
      for (const [label, value] of [['Due day',lesson.due],['Priority',lesson.priority],['Required sources',lesson.sources]]) {
        const term = document.createElement('dt'); term.textContent = label;
        const description = document.createElement('dd'); description.textContent = value; list.append(term, description);
      }
      card.append(list); cards.append(card);
    }
    host.append(cards);
  } else {
    const scroll = document.createElement('div'); scroll.className = 'table-scroll';
    const table = document.createElement('table');
    const caption = document.createElement('caption'); caption.textContent = 'Study assignments'; table.append(caption);
    const head = document.createElement('thead'); const row = document.createElement('tr');
    for (const label of ['Assignment','Due day','Priority','Sources']) { const th = document.createElement('th'); th.scope = 'col'; th.textContent = label; row.append(th); }
    head.append(row); table.append(head);
    const body = document.createElement('tbody');
    for (const lesson of lessons) {
      const tr = document.createElement('tr');
      for (const value of [lesson.name,lesson.due,lesson.priority,lesson.sources]) { const td = document.createElement('td'); td.textContent = value; tr.append(td); }
      body.append(tr);
    }
    table.append(body); scroll.append(table); host.append(scroll);
  }
}
function startTask(focus = true) {
  const context = $('context').value;
  const preference = $('preference').value;
  const learning = $('learning').checked;
  const choice = preference !== 'auto'
    ? { mode: preference, reason: `Using your ${preference} preference. Automatic selection is paused.` }
    : learning ? chooseMode(profile, context)
      : { mode: 'guided', reason: 'Learning is off. Automatic mode uses the guided view.' };
  const item = variants[context][sequence[context]++ % variants[context].length];
  task = { context, mode: choice.mode, item, errors: 0, hints: 0, learning, complete: false, elapsed: 0, activeSince: document.hidden ? null : performance.now() };
  started = true; taskNumber++;
  $('task-number').textContent = `PRACTICE ${taskNumber} · ${names[context].toUpperCase()}`;
  $('task-title').textContent = names[context];
  $('mode-badge').textContent = choice.mode === 'guided' ? 'Guided view' : 'Compact view';
  $('mode-reason').textContent = choice.reason;
  renderData(choice.mode);
  $('hint').textContent = item.hint; $('hint').hidden = true;
  $('hint-button').setAttribute('aria-expanded','false'); $('hint-button').disabled = false;
  $('question').textContent = item.question;
  $('answers').replaceChildren(...item.options.map((value,index) => {
    const label = document.createElement('label'); label.className = 'answer';
    const input = document.createElement('input'); input.type = 'radio'; input.name = 'answer'; input.value = value; input.required = true; input.id = `answer-${index}`;
    label.append(input,document.createTextNode(value)); return label;
  }));
  $('check').disabled = false; $('feedback').textContent = '';
  if (focus) $('task-title').focus();
}
function activeSeconds() {
  return (task.elapsed + (task.activeSince === null ? 0 : performance.now() - task.activeSince)) / 1000;
}
document.addEventListener('visibilitychange', () => {
  if (!started || task.complete) return;
  if (document.hidden && task.activeSince !== null) { task.elapsed += performance.now() - task.activeSince; task.activeSince = null; }
  else if (!document.hidden && task.activeSince === null) task.activeSince = performance.now();
});
$('answer-form').addEventListener('submit', event => {
  event.preventDefault(); if (task.complete) return;
  const value = new FormData(event.currentTarget).get('answer');
  if (value !== task.item.answer) { task.errors++; $('feedback').textContent = 'Try again. Check the assignment information above.'; return; }
  task.complete = true;
  const seconds = activeSeconds(); let message = `Correct. Finished in ${seconds.toFixed(1)} active seconds with ${task.errors} incorrect attempt${task.errors === 1 ? '' : 's'}.`;
  if (task.learning && $('learning').checked) {
    try {
      const result = recordOutcome(profile, task.context, task.mode, { seconds, errors: task.errors, hints: task.hints });
      persist(); renderStatistics(); message += ` Reward ${result.reward.toFixed(2)} recorded for ${task.mode}. Start the next task to see the next view.`;
    } catch { message += ' The model could not record this outcome. Clear learned data to restart.'; }
  } else message += ' No learning outcome recorded. Start the next task when ready.';
  $('feedback').textContent = message;
  $('check').disabled = true; $('hint-button').disabled = true;
});
$('hint-button').addEventListener('click', () => {
  if (!task.complete && $('hint').hidden) { task.hints++; $('hint').hidden = false; $('hint-button').setAttribute('aria-expanded','true'); }
});
$('next').addEventListener('click', () => startTask());
for (const id of ['preference','context','learning']) $(id).addEventListener('change', () => {
  // Disabling consent also cancels collection for the task already in progress.
  if (id === 'learning' && !$('learning').checked) task.learning = false;
  $('mode-reason').textContent = 'Your new settings will apply when you start the next task. The current view stays in place.';
});
$('reset').addEventListener('click', () => {
  profile = createProfile(); task.learning = false; // Avoid repopulating a cleared model from the current task.
  try { localStorage.removeItem(key); } catch { persistent = false; }
  renderStatistics(); storageStatus();
  $('mode-reason').textContent = 'Learned data cleared. The current task stays in place; start the next task to begin again.';
});
storageStatus(); renderStatistics(); startTask(false);
