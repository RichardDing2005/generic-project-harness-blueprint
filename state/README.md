# State

`state/` stores the **current execution pointer**.

It is intentionally small.

## What belongs in state

- bootstrap mode flag
- current formal stage
- current subflow position, if any
- current pipeline anchors
- active memory references
- latest snapshot reference, if any
- required config references
- required artifact references
- blocking status
- next action
- latest verification result

## What does not belong in state

Do not store:
- long reasoning
- repeated historical logs
- full stage analysis
- giant artifact summaries
- full configuration values

Those belong in `memory/` or `config/`.

## Authority rule

`state/CURRENT_STATE.json` is the authoritative runtime pointer for the current round.

If `memory/index.json` disagrees with state, execution follows state first and the mismatch must be reconciled.
