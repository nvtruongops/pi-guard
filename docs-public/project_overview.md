# Project Overview

## Scope boundary declaration

This is a project-authored public summary. It is not an official registration record, assessment rubric, or institutional document.

## Research topic

PI-Guard studies an external text-inspection layer for applications that use large language models. The research explores how a guardrail can distinguish ordinary requests from prompt-injection and jailbreak attempts before a request reaches a downstream model.

## System boundary

The proposed guardrail evaluates submitted text at the application boundary. It does not inspect the downstream model's private weights, hidden state, or internal execution. The project treats detection and routing as risk-mitigation mechanisms; it does not claim that any classifier can make an application completely secure.

## Evidence and limitations

Research claims and implementation results are reported with their supporting sources, data, and execution evidence. Proposed design goals are kept distinct from measured outcomes, and limitations are stated alongside conclusions.

## Publication boundary

This summary omits registration fields, institutional assessment rules, schedules, personal names, student identifiers, and contact details. The detailed research record and source code remain in the project's research repository.
