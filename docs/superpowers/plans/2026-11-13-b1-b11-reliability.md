# b1–b11 Reliability and Latency Implementation Plan

> **For agentic workers:** Use the executing-plans workflow to implement this plan task by task. Steps use checkbox syntax for tracking.

**Goal:** Reduce avoidable b1–b11 failures and waiting while preserving the active per-device session and never repeating an uncertain Amazon action.

**Architecture:** Keep the existing Swarmote ADB driver, GUI, q1/q2 routes, and per-device session model. Add timing evidence and typed recovery behavior around the existing step runner, reuse one verified UI snapshot where safe, and make each b1–b11 step reconcile its current screen before retrying. Tune wait intervals only after capturing baseline latency.

**Tech Stack:** Existing Python 3.11+, Swarmote ADB, `unittest`, current `PostMenuSession` and `build_common_steps`.

**Spec:** User request: plan reliability work for all b1–b11, including timeout handling and long inter-step waits; do not change the production code before plan review.

## Global Constraints

- Keep the current ADB driver as the production driver; no UiAutomator2 migration in this work.
- Keep the CustomTkinter GUI, Swarmote Profile handling, per-machine serial mapping, and current q1/q2 screen flow.
- Do not reset, close, or replace an active q1 session or discard data held in memory.
- Never log phone numbers, passwords, full OTPs, card details, or OTP URLs/tokens.
- Retry read-only operations automatically; reconcile the live screen before retrying any action that may have changed Amazon state.
- Use existing `unittest`; do not add `pytest` as a dependency.
- Pilot only on a safe, user-designated device/screen. Do not use the q1 session while the user is actively working on it.

## Review Focus

- ADB command times out after Android received a tap: read the screen before any retry; do not duplicate Continue, SMS, or Create.
- XML dump is incomplete or slow: bounded read retry with remaining-time awareness; do not convert one transient read failure into a whole-session reset.
- Same label appears more than once or layout differs from the saved screenshots: keep the machine at that screen and report the exact unresolved step.
- Keyboard, scrolling, or animation changes bounds after a read: take a fresh snapshot before tapping; do not reuse stale coordinates.
- OTP page is delayed, stale, challenged, or unavailable: preserve the SMS step and OTP status, retry only the read path, and never send another SMS automatically.

## File Map

- Modify `amazon_android/post_menu.py` for per-step timing and shared recovery policy; retain one `PostMenuSession` per machine.
- Modify `amazon_android/account_flow.py` for reusable UI snapshots, explicit before/after conditions, and safe retry/reconciliation for b4–b11.
- Modify `amazon_android/q1_flow.py` and `amazon_android/q2_flow.py` only for the unique b1–b3 conditions and redundant waits confirmed by the baseline.
- Extend existing `tests/test_post_menu.py`, `tests/test_q1_flow.py`, and `tests/test_q2_flow.py`; add an `account_flow` unittest file only if existing files cannot isolate a behavior.
- Update `POST_MENU_REQUIREMENTS.md`, `FLOW_PROGRESS.md`, and `PROJECT_HANDOFF.md` with measured results and remaining device-only checks.

---

### Task 1: Measure current step latency and classify existing failures

**Files:**
- Modify: `amazon_android/post_menu.py`
- Modify: `amazon_android/account_flow.py`
- Test: `tests/test_post_menu.py`
- Test: `tests/test_q1_flow.py`
- Test: `tests/test_q2_flow.py`

**Interfaces:**
- Emit a per-step diagnostic record containing machine slot, step name, elapsed time, read/tap/type/wait counts, and sanitized error category.
- Do not include serial, account row contents, OTP URL, SMS body, or field values in the diagnostic record.

- [ ] Add unittest coverage that asserts diagnostic output contains timing/category but excludes account secrets and OTP values.
- [ ] Capture baseline timings for each step and each ADB operation on an available safe pilot; report median and p95, timeout count, and screen-read failures.
- [ ] Separate code-path analysis from device evidence: mark unavailable measurements as NOT RUN rather than estimating them.

**Acceptance:** There is a baseline report identifying which waits dominate b1–b11 and a per-step error count without sensitive data.

### Task 2: Define safe retry, reconcile, pause, and stop behavior

**Files:**
- Modify: `amazon_android/post_menu.py`
- Modify: `tests/test_post_menu.py`

**Interfaces:**
- Add a typed step failure category distinguishing transient read/ADB timeout, unknown or ambiguous screen, action result uncertain, invalid input, and user stop.
- Keep `PostMenuSession.run(...)` as the owner of the machine's attempt deadline, current step, and paused state.

- [ ] Add tests for transient read retry, hard-stop conditions, user cancellation during retry, and deadline expiry preserving the same `next_step` and session data.
- [ ] Retry only idempotent reads with a bounded policy derived from measured p95 latency and remaining attempt time.
- [ ] On a timeout after a state-changing command may have landed, reconcile by reading the live screen before deciding whether to continue or pause.
- [ ] On hard deadline, keep the machine paused at the same step with an actionable reason; never clear the batch or advance the step.

**Acceptance:** A transient timeout no longer immediately abandons a safe read; no uncertain tap is automatically replayed; expiry preserves the resumable session.

### Task 3: Reduce redundant UI reads and unnecessary waits

**Files:**
- Modify: `amazon_android/account_flow.py`
- Modify: `amazon_android/q1_flow.py`
- Modify: `amazon_android/q2_flow.py`
- Test: `tests/test_q1_flow.py`
- Test: `tests/test_q2_flow.py`

**Interfaces:**
- Represent one UI read as a snapshot scoped to a single action/reconciliation; share it among selectors until a tap, type, scroll, or screen transition invalidates it.
- Do not share snapshots across devices or across state-changing actions.

- [ ] Add tests proving one snapshot is reused within a step and invalidated after each state-changing action.
- [ ] Remove fixed sleeps only when an explicit screen/element condition already proves the transition; preserve q2's documented 2–5 second Home visit.
- [ ] Use measured p95 read/transition latency to set short polling intervals and bounded backoff; do not lower intervals below the time needed for an ADB read.
- [ ] Benchmark b1–b11 again against Task 1 using the same device, screen, and action sequence.

**Acceptance:** Duplicate `uiautomator dump`/`cat` work is reduced where safe, and p95 step time improves without weakening screen checks.

### Task 4: Make b1–b11 recovery explicit and idempotent

**Files:**
- Modify: `amazon_android/account_flow.py`
- Modify: `amazon_android/q1_flow.py`
- Modify: `amazon_android/q2_flow.py`
- Test: `tests/test_q1_flow.py`
- Test: `tests/test_q2_flow.py`

**Interfaces:**
- Each step declares recognized starting states, success states, safe read retry conditions, and whether the action may be repeated after reconciliation.
- Preserve separate q1/q2 b1–b3 actions and the shared b4–b11 flow.

- [ ] Add fixtures from the supplied q1/q2 screenshots for supported screen variants and known ambiguous layouts; do not infer unseen screens.
- [ ] Cover b1–b3 navigation retries and b4–b9 input/transition reconciliation, including duplicate labels, keyboard-open layouts, and stale bounds.
- [ ] Cover b10 and b11 so a timeout never repeats Send code by SMS or Create; after a stop/retry, inspect the screen and resume at the safe next action.
- [ ] Cover both success and failure of each UI transition and ensure one device's failure does not stop another device.

**Acceptance:** Every documented variant has a deterministic test; ambiguous screens pause only the affected machine with step-specific evidence.

### Task 5: Tune deadlines and verify on a safe pilot before q1/q2

**Files:**
- Modify: `POST_MENU_REQUIREMENTS.md`
- Modify: `FLOW_PROGRESS.md`
- Modify: `PROJECT_HANDOFF.md`

- [ ] Choose per-step soft limits and a per-attempt hard limit from measured q3/pilot timings plus a documented safety margin; do not merely raise all timeouts globally.
- [ ] If q3 is available and designated safe, run repeated read-only pilot measurements there first. Otherwise wait for a safe device/tunnel; do not interrupt the active q1 flow.
- [ ] After the pilot passes and the user confirms q1 is idle, repeat the same read-only comparison on q1 and then q2 as the project spec requires.
- [ ] Report before/after median and p95 latency, success/error rates, correct serial, supported screen variants, and any action not verified on device.
- [ ] Keep ADB as the production driver unless measured evidence shows a clear reliability gain; any driver replacement is a separate reviewed plan.

**Acceptance:** The report distinguishes unit/mock results from real-device results and contains enough evidence to choose ADB, UiAutomator2, or a hybrid approach.

## Completion Criteria

- Timeouts on read-only operations retry safely within bounded limits.
- Any state-changing action with uncertain delivery is reconciled from live UI before retry.
- Session state and user-entered data remain intact across a timeout/pause.
- No screen/action is selected from a stale snapshot or static screenshot coordinate.
- Measured p95 wait/step latency is lower than baseline or the report explains why it cannot be reduced safely.
- q1/q2 flows and GUI behavior have no regression in tests; real-device results are reported separately.
