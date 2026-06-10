# Repository Guidance

Fork of the upstream OpenAI Privacy Filter (OPF): a local-only PyTorch
token-classification model (1.5B params, BIOES span labels over 8 PII
categories) with the `opf` CLI for redaction, eval, and finetuning.

## Definition of Done
- Before reporting any code change as complete, run `python3 -m unittest discover tests` and report the actual output (test count and OK/FAILED).
- If anything fails: paste the failure verbatim, do not claim success, do not weaken, skip, or delete the failing test to get green.
- If a command cannot run (missing dep, sandbox limit), report the exact error and stop; do not work around it silently and do not report done.

## Hard Prohibitions
- This is a FORK. `origin` is the upstream openai repo; `fork` is the personal remote. NEVER push to `origin`. Push branches to `fork` only.
- Keep local changes minimal and rebase-friendly: branch from `main`, no drive-by refactors of upstream code, no formatting sweeps. Open PRs against upstream only when explicitly asked.
- Running `opf` redaction, eval, or finetuning with no checkpoint at `$OPF_CHECKPOINT` or `~/.opf/privacy_filter` downloads ~1.5B-param weights from Hugging Face. Do NOT trigger that in sandboxed or metered environments unless the user asks. To verify behavior, use the unit tests; they never load the model.
- `memory/` and `.claude/` are gitignored on purpose (local-only notes). Never force-add them.

## Project Shape
- Entry point: `opf` console script, equivalent to `python -m opf` (`opf/__main__.py`). Modes: one-shot redaction (arg, `-f` file, piped stdin, or interactive), `opf eval <dataset.jsonl>`, finetuning.
- Source under `opf/`: `_cli/` (arg parsing, rendering), `_core/` (decoding, runtime, sequence labeling, spans), `_model/`, `_eval/`, `_train/`, `_common/`, `_api.py`.
- Docs at repo root: `README.md`, `FINETUNING.md`, `EVAL_AND_OUTPUT_MODES.md`, `OUTPUT_SCHEMAS.md`. Finetuning demo scripts: `examples/scripts/finetuning/`; toy datasets: `examples/data/`.

## Commands
- Tests: `python3 -m unittest discover tests` (7 tests in `tests/test_cli_args.py`, fast, no checkpoint or GPU needed).
- Install: `pip install -e .` (Python >= 3.10; deps: torch, safetensors, tiktoken, huggingface_hub, numpy, packaging).
- No lint, typecheck, or CI config exists. Do not invent or add tooling configs without being asked.

## Working Rules
- Changing redaction CLI flags: edit `build_redaction_parser` in `opf/__main__.py`; stdin/input framing lives in `iter_inputs` in `opf/_cli/args.py`. Tests mock `sys.stdin`, so keep `iter_inputs` importable and side-effect free.
- Handling multi-paragraph stdin: piped stdin defaults to one input per non-empty line (`--stdin-mode line`); use `--stdin-mode whole` when spans need context across line breaks. This flag is a local addition on `feat/stdin-mode-whole`, not yet upstream; do not assume it exists on `main` or upstream.
- Running anything that loads the model on a machine without a GPU: pass `--device cpu` (GPU is the default).
- Hitting a blocker (missing checkpoint, permission, network): report the exact command and error to the user; do not substitute a guess for a verified result.

## Memory Handoff
At the end of any substantial task, write a handoff note to
`.claude/memory-handoffs/` using that directory's `TEMPLATE.md`. Record
durable discoveries, gotchas, and decisions. Do not wait to be reminded.
