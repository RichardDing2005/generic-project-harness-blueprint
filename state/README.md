# State

`state/` stores the **current execution pointer**.

It is intentionally small.

## What belongs in state

- current stage
- current subflow position
- current pipeline anchors
- active memory references
- latest snapshot reference
- blocking status
- next action
- latest verification result

## What does not belong in state

Do not store:
- long reasoning
- repeated historical logs
- full stage analysis
- giant artifact summaries

Those belong in `memory/`.
