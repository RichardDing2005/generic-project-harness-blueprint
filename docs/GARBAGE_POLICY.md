# Garbage Policy

## 1. Purpose

`garbage/` is not a trash can for careless deletion.  
It is a **controlled retirement area** for:

- invalidated artifacts,
- superseded verbose reports,
- failed run outputs no longer needed in active memory,
- obsolete intermediate materials.

## 2. What belongs here

Suitable garbage candidates:

- failed smoke artifacts after the failure lesson is preserved,
- obsolete diagnostic outputs replaced by a newer accepted run,
- superseded exploratory reports,
- abandoned branches or work products,
- overly long analysis logs whose conclusions have already been promoted.

## 3. What does not belong here

Do not send these to garbage unless replaced elsewhere:

- the active stage summary,
- the latest accepted snapshot,
- current state,
- the only record of a meaningful decision,
- the only record of a project lesson.

## 4. Required bookkeeping

Every move into `garbage/` must create:

1. a physical archived file or record,
2. an entry in `garbage/index.json`,
3. a retirement reason,
4. an optional `replacement_ref`,
5. an optional `derived_lesson_ref`,
6. an optional `superseded_by`,
7. a `can_restore` flag.

## 5. Retention model

Garbage is retained for traceability, not for active reasoning.

The core loop should not read `garbage/` unless:
- a traceability question arises,
- a contradiction needs backtracking,
- a user explicitly asks for retired material.
