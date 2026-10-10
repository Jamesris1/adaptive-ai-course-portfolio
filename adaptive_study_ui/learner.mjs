/**
 * Contextual upper-confidence-bound action selection is based on the bandit
 * concepts in Sutton and Barto (2018), Reinforcement Learning: An Introduction,
 * and the UCB1 selection rule of Auer, Cesa-Bianchi, and Fischer (2002).
 * Only counts and mean rewards are stored; no answers or event logs are retained.
 */

const CONTEXTS = Object.freeze(['deadline', 'priority', 'requirements']);
const MODES = Object.freeze(['guided', 'compact']);
const MAX_COUNT = 100000;

function object(value) {
  return value !== null && typeof value === 'object' && !Array.isArray(value);
}

function validProfile(profile) {
  if (!object(profile) || profile.version !== 1 || !object(profile.contexts)) return false;
  if (Object.keys(profile).length !== 2 || Object.keys(profile.contexts).length !== CONTEXTS.length) return false;
  for (const context of CONTEXTS) {
    const state = profile.contexts[context];
    if (!object(state) || Object.keys(state).length !== MODES.length) return false;
    for (const mode of MODES) {
      const arm = state[mode];
      if (!object(arm) || Object.keys(arm).length !== 2) return false;
      if (!Number.isInteger(arm.count) || arm.count < 0 || arm.count > MAX_COUNT) return false;
      if (!Number.isFinite(arm.mean) || arm.mean < 0 || arm.mean > 1) return false;
      if (arm.count === 0 && arm.mean !== 0) return false;
    }
  }
  return true;
}

function validateContext(context) {
  if (!CONTEXTS.includes(context)) throw new RangeError('Unknown task context.');
}

function validateMode(mode) {
  if (!MODES.includes(mode)) throw new RangeError('Unknown interface mode.');
}

function requireProfile(profile) {
  if (!validProfile(profile)) throw new TypeError('Invalid learning profile; reset it before continuing.');
}

export function createProfile() {
  return {
    version: 1,
    contexts: Object.fromEntries(CONTEXTS.map(context => [context,
      Object.fromEntries(MODES.map(mode => [mode, { count: 0, mean: 0 }]))
    ]))
  };
}

/** Recover only the small, supported aggregate schema from local storage. */
export function sanitizeProfile(input) {
  if (!validProfile(input)) return createProfile();
  const profile = createProfile();
  for (const context of CONTEXTS) {
    for (const mode of MODES) {
      profile.contexts[context][mode].count = input.contexts[context][mode].count;
      profile.contexts[context][mode].mean = input.contexts[context][mode].mean;
    }
  }
  return profile;
}

/**
 * Reward is an explicit classroom design choice, not a validated UX measure.
 * Time, incorrect attempts, and hint requests reduce the score, with caps so
 * that a single factor cannot consume the complete reward.
 */
export function rewardFor(outcome) {
  if (!object(outcome)) throw new TypeError('An outcome object is required.');
  const { seconds, errors, hints } = outcome;
  if (!Number.isFinite(seconds) || seconds < 0) throw new RangeError('Seconds must be finite and nonnegative.');
  if (!Number.isSafeInteger(errors) || errors < 0) throw new RangeError('Errors must be a nonnegative integer.');
  if (!Number.isSafeInteger(hints) || hints < 0) throw new RangeError('Hints must be a nonnegative integer.');
  return Math.max(0, Math.min(1,
    1 - Math.min(seconds / 60, 0.6) - Math.min(errors * 0.15, 0.3) - Math.min(hints * 0.05, 0.1)
  ));
}

/**
 * Each task context has independent two-arm UCB estimates. The guided arm is
 * tried first, followed by compact. Later choices combine observed mean reward
 * and exploration: mean + sqrt(2 * ln(total observations) / arm observations).
 */
export function chooseMode(profile, context) {
  requireProfile(profile);
  validateContext(context);
  const arms = profile.contexts[context];
  for (const mode of MODES) {
    if (arms[mode].count === 0) {
      return {
        mode,
        reason: `Trying ${mode} for this task because it has no recorded outcomes yet.`
      };
    }
  }
  const total = arms.guided.count + arms.compact.count;
  const score = mode => arms[mode].mean + Math.sqrt(2 * Math.log(total) / arms[mode].count);
  const mode = score('guided') >= score('compact') ? 'guided' : 'compact';
  return {
    mode,
    reason: `Selected ${mode} using this task's mean rewards and an exploration allowance. Both layouts continue to be considered.`
  };
}

/** Record a completed task, including outcomes from a manually chosen layout. */
export function recordOutcome(profile, context, mode, outcome) {
  requireProfile(profile);
  validateContext(context);
  validateMode(mode);
  const reward = rewardFor(outcome);
  const arm = profile.contexts[context][mode];
  if (arm.count === MAX_COUNT) throw new RangeError('The learning profile has reached its observation limit; reset learning.');
  arm.count += 1;
  arm.mean += (reward - arm.mean) / arm.count;
  return { reward, count: arm.count, mean: arm.mean };
}
