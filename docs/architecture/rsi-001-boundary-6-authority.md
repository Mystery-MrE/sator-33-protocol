# RSI-001 Boundary #6: Evidence Does Not Confer Authority

## Status

**Boundary #6 is structurally resolved** when an implementation preserves all of
these rules:

1. Evidence and authority are separate domains.
2. Authority originates from an independently established source.
3. No evidence or derived state silently promotes itself into authority.

This boundary defines the non-derivability of authority from evidence. It does
not define a complete authorization protocol, authorization lifecycle, or
execution gate.

## 6.1 Evidence domain (`E`)

The evidence domain contains facts and representations supplied to an evaluator,
observed during processing, or mechanically established. It includes:

- Raw reference bytes and their integrity results.
- `item_identity` and declaration facts.
- Availability and completion facts.
- Provenance and temporal metadata.
- Signatures and other supplied artifacts.
- Parsed, derived, or reconstructed representations.
- Explicitly recorded absence, conflict, and uncertainty.

Evidence records what is supplied, observed, or mechanically established; it
does **not** independently determine what actions are permitted. The presence
of an evidence fact MUST NOT be interpreted as an authorization decision unless
an applicable authority-bearing rule explicitly establishes that relationship.

## 6.2 Authority domain (`A`)

Authority is established by an external, explicitly identified source, for
example:

- a relying-party policy;
- an applicable protocol rule;
- an authorized policy issuer;
- a separately established authorization state; or
- a designated decision authority.

The authority source MUST be identifiable independently of the evidence under
evaluation and MUST be bound to an identifiable applicable policy or authority
contract. Supplying a policy from the relying party is one valid implementation
pattern, but it is not the only one: a statically compiled protocol rule,
authenticated configuration, or another explicitly authorized mechanism may
supply authority.

The following are evidence, rather than authority sources, merely because they
appear in a reference bundle:

- `item_identity`
- `content_digest`
- `integrity_binding`
- `provenance`
- `temporal_metadata`
- `signature_artifact`
- `declared_policy`
- `declared_authorization`

A submitted declaration of authority is evidence about what was declared. It is
not, by itself, proof that the declaration is authoritative.

## 6.3 Evaluation predicates

| Predicate | Meaning |
| --- | --- |
| `P_E(e)` | Evidence fact or representation `e` is present in the evaluation input. |
| `P_I(i)` | The required integrity relationship is established for item `i`. |
| `P_A(a)` | Authority source `a` is independently established and applicable. |
| `P_C(c)` | Evaluation context `c` is established under the applicable contract. |
| `P_Eval(A, E, C)` | An authority-bearing evaluator produces a defined result. |

These predicates are intentionally separate. `P_I(i) = TRUE` means only that
the applicable integrity relationship was established; it does not imply
`P_A(a) = TRUE`. Conversely, `P_A(a) = TRUE` does not imply that any evidence
item is valid, complete, or admissible.

## 6.4 Authority evaluation

The relying party or applicable authority-bearing protocol component supplies
the evaluator with independently established authority, evidence, and explicit
context:

```text
Evaluate(A, E, C) -> V
```

Where `V` is the defined evaluation result, including its applicable scope. The
evaluator MUST:

- receive an independently established authority source;
- receive the evidence to be evaluated;
- apply explicitly defined policy and evaluation rules;
- produce a defined result with its applicable scope; and
- preserve the distinction between evidence facts and the resulting authority
  judgment.

An evaluator MUST NOT derive authority solely from `E` or a subset of evidence,
including a valid digest, valid signature, provenance record, or declaration of
permission.

## 6.5 Evidence--authority non-promotion invariant

> No evidence fact, collection of evidence facts, derived representation,
> integrity result, provenance record, temporal record, or submitted declaration
> may independently establish, expand, or confer authority. Authority MUST
> originate from an independently established authority source and may be
> applied to evidence only through an explicitly defined evaluation rule.

The following implication is prohibited:

```text
E = TRUE  ->  A = TRUE
```

unless an independently established rule explicitly defines and authorizes that
relationship. Even in that case, the resulting authority judgment belongs to
the evaluator and its policy, not to the evidence artifact itself.

## 6.6 Signature-specific prohibition

A valid signature is not an execution authorization:

```text
valid_signature(bytes) != authorized_to_execute(bytes)
```

More formally, `P_SignatureValid(x) = TRUE` MUST NOT alone establish
`P_ExecutionAuthorized(x) = TRUE`. Execution authorization requires an
applicable authority rule, which may additionally consider signer authorization
and scope, policy version, subject and intended operation, revocation or
temporal constraints, required evidence, environmental restrictions, and
explicit authorization state. Those requirements belong to the relevant
authorization protocol, not automatically to RSI-001.

## 6.7 No silent promotion of derived state

Derived state MUST remain distinguishable from supplied evidence and authority
decisions. An implementation MUST NOT silently promote any of the following:

- `parsed_state`
- `normalized_state`
- `cache_entry`
- `inferred_status`
- `successful_retrieval`
- `local_configuration`
- `diagnostic_result`

into `authorized`, `trusted`, `qualified`, `admissible`, or
`valid_for_execution`. Such a transition requires an explicitly defined rule,
an identifiable authority source, and a recorded evaluation result.

## 6.8 Failure and unresolved semantics

When the authority source is absent, ambiguous, inapplicable, or cannot be
established, RSI-001 MUST NOT infer authorization from the available evidence.
It MUST preserve the distinction between
`REFERENCE_STATE_INTEGRITY_ESTABLISHED` and `AUTHORITY_ESTABLISHED`: the former
is a narrow reference-state integrity result, not an authorization result.

When the authority determination is outside RSI-001's scope or lacks the
required authority inputs, the result remains outside RSI-001's authority
claim. The downstream authority protocol represents that condition using its
defined unresolved or unavailable state. RSI-001 MUST NOT invent a universal
authorization failure code.

## 6.9 Normative model

```text
Reference state -> evidence facts E -- evaluated against -->
independently established authority A -- under context C -->
explicit evaluator -> authority judgment V
```

The following architecture is prohibited:

```text
Reference bytes -> valid digest or signature -> implicit trust -> execution permission
```

## 6.10 Conformance cases

| Case | Expected result |
| --- | --- |
| Valid digest, no authority source | No authorization is established. |
| Valid signature, no signer-scope policy | No execution authorization is established. |
| Submitted `authorized=true` declaration | The declaration is evidence, not authority. |
| Independently supplied policy and matching evidence | The evaluator may produce a defined authority result. |
| Valid integrity and a failed policy condition | Integrity remains established; authorization does not follow. |
| Valid evidence and missing authority context | No silent promotion; the authority result is unresolved or out of scope. |
| Derived cache reports `trusted` | The cache cannot independently establish authority. |
| Authority source changes | A new evaluation is required under the applicable policy and version. |
