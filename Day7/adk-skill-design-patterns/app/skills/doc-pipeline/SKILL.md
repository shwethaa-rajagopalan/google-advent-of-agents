---
name: doc-pipeline
description: Generates API documentation from Python source code through a multi-step pipeline. Use when the user asks to document a module, generate API docs, or create documentation from code.
metadata:
  pattern: pipeline
  steps: "4"
---

You are running a documentation generation pipeline. Execute each step in order. Do NOT skip steps or proceed if a step fails.

## Step 1 — Parse & Inventory

Analyze the user's Python code to extract:
- All public classes and their methods
- All public functions
- All module-level constants
- Existing docstrings (note which are missing)

Present the inventory to the user as a checklist. Ask: "Is this the complete public API you want documented?"

## Step 2 — Generate Docstrings

For each public function/method that lacks a docstring:
- Load 'references/docstring-style.md' for the required format
- Generate a docstring following the style guide exactly
- Present each generated docstring for user approval

Do NOT proceed to Step 3 until the user confirms the docstrings.

## Step 3 — Assemble Documentation

Load 'assets/api-doc-template.md' for the output structure.

Compile all classes, functions, and their docstrings into a single API reference document following the template.

Include:
- Table of contents with anchor links
- Each class/function in its own section
- Parameters, return types, and examples for each

## Step 4 — Quality Check

Review the assembled document against 'references/quality-checklist.md':
- Every public symbol is documented
- Every parameter has a type and description
- At least one usage example per function
- No placeholder text remains

Report the quality check results. If issues found, fix them before presenting the final document.
