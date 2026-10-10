import assert from 'node:assert/strict';
import { createProfile, chooseMode, recordOutcome, sanitizeProfile, rewardFor } from './learner.mjs';

let passed = 0;
const near = (actual, expected) => assert.ok(Math.abs(actual - expected) < 1e-12, `${actual} != ${expected}`);
const ideal = { seconds: 0, errors: 0, hints: 0 };
function test(name, body) {
  body();
  passed += 1;
  console.log(`PASS ${name}`);
}

test('New tasks explore guided and compact before comparing rewards', () => {
  const profile = createProfile();
  assert.equal(chooseMode(profile, 'deadline').mode, 'guided');
  recordOutcome(profile, 'deadline', 'guided', ideal);
  assert.equal(chooseMode(profile, 'deadline').mode, 'compact');
  recordOutcome(profile, 'deadline', 'compact', ideal);
  assert.equal(chooseMode(profile, 'deadline').mode, 'guided');
});

test('The online estimate equals the mean of completed task rewards', () => {
  const profile = createProfile();
  const observations = [ideal, { seconds: 12, errors: 1, hints: 1 }, { seconds: 36, errors: 2, hints: 2 }];
  const expected = observations.map(rewardFor).reduce((sum, reward) => sum + reward, 0) / observations.length;
  for (const outcome of observations) recordOutcome(profile, 'priority', 'compact', outcome);
  assert.equal(profile.contexts.priority.compact.count, 3);
  near(profile.contexts.priority.compact.mean, expected);
});

test('Learning is isolated by task context and selected layout', () => {
  const profile = createProfile();
  recordOutcome(profile, 'deadline', 'guided', ideal);
  assert.deepEqual(profile.contexts.priority, createProfile().contexts.priority);
  assert.deepEqual(profile.contexts.requirements, createProfile().contexts.requirements);
  assert.deepEqual(profile.contexts.deadline.compact, { count: 0, mean: 0 });
  assert.equal(chooseMode(profile, 'requirements').mode, 'guided');
});

test('Synthetic biased outcomes lead to more trials of the higher reward layout', () => {
  const profile = createProfile();
  for (let round = 0; round < 200; round += 1) {
    const { mode } = chooseMode(profile, 'deadline');
    const outcome = mode === 'guided'
      ? { seconds: 6, errors: 0, hints: 0 }
      : { seconds: 42, errors: 1, hints: 1 };
    recordOutcome(profile, 'deadline', mode, outcome);
  }
  const { guided, compact } = profile.contexts.deadline;
  assert.ok(guided.count > 3 * compact.count);
  assert.ok(compact.count > 1, 'UCB must continue exploring the lower reward arm.');
  near(guided.mean, 0.9);
  near(compact.mean, 0.2);
  assert.equal(chooseMode(profile, 'deadline').mode, 'guided');
});

test('An under-sampled layout can be explored despite its lower mean', () => {
  const profile = createProfile();
  profile.contexts.priority.guided = { count: 100, mean: 0.9 };
  profile.contexts.priority.compact = { count: 1, mean: 0.1 };
  assert.equal(chooseMode(profile, 'priority').mode, 'compact');
});

test('Reward values remain bounded and each penalty saturates', () => {
  near(rewardFor(ideal), 1);
  near(rewardFor({ seconds: 6, errors: 1, hints: 1 }), 0.7);
  near(rewardFor({ seconds: 60, errors: 10, hints: 10 }), 0);
  near(rewardFor({ seconds: Number.MAX_VALUE, errors: Number.MAX_SAFE_INTEGER, hints: Number.MAX_SAFE_INTEGER }), 0);
});

test('Invalid task outcomes are rejected without mutating estimates', () => {
  const profile = createProfile();
  const invalid = [null, {}, { ...ideal, seconds: NaN }, { ...ideal, seconds: Infinity }, { ...ideal, seconds: -1 },
    { ...ideal, errors: -1 }, { ...ideal, errors: 0.5 }, { ...ideal, errors: '1' }, { ...ideal, hints: Infinity }];
  for (const outcome of invalid) assert.throws(() => recordOutcome(profile, 'deadline', 'guided', outcome));
  assert.deepEqual(profile, createProfile());
});

test('Unknown contexts, unknown modes, and corrupted profiles are rejected', () => {
  const profile = createProfile();
  assert.throws(() => chooseMode(profile, 'unknown'));
  assert.throws(() => recordOutcome(profile, 'deadline', 'unknown', ideal));
  assert.throws(() => recordOutcome(profile, 'unknown', 'guided', ideal));
  assert.throws(() => chooseMode({}, 'deadline'));
  assert.throws(() => recordOutcome({}, 'deadline', 'guided', ideal));
  assert.deepEqual(profile, createProfile());
});

test('Valid persisted statistics are recovered as an independent copy', () => {
  const original = createProfile();
  recordOutcome(original, 'requirements', 'compact', ideal);
  const recovered = sanitizeProfile(JSON.parse(JSON.stringify(original)));
  assert.deepEqual(recovered, original);
  recordOutcome(recovered, 'requirements', 'compact', { seconds: 30, errors: 1, hints: 1 });
  assert.equal(original.contexts.requirements.compact.count, 1);
  assert.equal(recovered.contexts.requirements.compact.count, 2);
});

test('Corrupt or oversized stored profiles reset to an empty bounded profile', () => {
  const invalid = [null, [], {}, { version: 99, contexts: {} }];
  for (const patch of [{ count: -1 }, { count: 0.5 }, { count: 100001 }, { mean: NaN }, { mean: Infinity },
    { mean: 1.01 }, { count: 0, mean: 0.5 }, { count: '1' }]) {
    const profile = createProfile();
    Object.assign(profile.contexts.deadline.guided, patch);
    invalid.push(profile);
  }
  const withLog = createProfile();
  withLog.events = ['unnecessary personal data'];
  invalid.push(withLog);
  for (const candidate of invalid) assert.deepEqual(sanitizeProfile(candidate), createProfile());
});

test('Observation limits reject writes without changing the profile', () => {
  const profile = createProfile();
  profile.contexts.deadline.guided = { count: 100000, mean: 0.5 };
  const before = JSON.stringify(profile);
  assert.throws(() => recordOutcome(profile, 'deadline', 'guided', ideal), /limit/);
  assert.equal(JSON.stringify(profile), before);
  assert.deepEqual(sanitizeProfile(profile), profile);
});

test('Manual layout choices update the chosen arm using only aggregate values', () => {
  const profile = createProfile();
  const result = recordOutcome(profile, 'requirements', 'compact', { seconds: 18, errors: 0, hints: 1 });
  near(result.reward, 0.65);
  assert.equal(result.count, 1);
  assert.deepEqual(Object.keys(profile).sort(), ['contexts', 'version']);
  assert.deepEqual(Object.keys(profile.contexts.requirements.compact).sort(), ['count', 'mean']);
  assert.equal(chooseMode(profile, 'requirements').mode, 'guided');
});

console.log(`\n${passed} tests passed. Synthetic learning tests demonstrate algorithm behavior, not measured user benefit.`);
