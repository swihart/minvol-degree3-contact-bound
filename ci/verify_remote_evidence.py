#!/usr/bin/env python3
"""Validate the recorded rc1 remote, hosted-CI, and fresh-clone evidence."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EVIDENCE = ROOT / "certificate" / "evidence" / "rc1_remote_audit.json"
HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")

EXPECTED_JOBS = {
    "Exact certificate, audits, metadata, release docs, and paper reconciliation",
    "Independent base-R audit",
    "Build and preflight paper and documentation PDFs",
}

DOCS_WITH_COMMIT_AND_RUN = (
    ROOT / "CLEAN_CLONE_CHECK.md",
    ROOT / "VERIFICATION_STATUS.md",
    ROOT / "certificate" / "INDEPENDENT_AUDIT.md",
    ROOT / "proof" / "PROOF_LEDGER.md",
    ROOT / "RELEASE_CHECKLIST.md",
)

STALE_PHRASES = (
    "(not yet created)",
    "has not yet been pushed to the intended public repository",
    "hosted run pending",
    "public-remote clone and hosted workflow record remain pending",
)


def fail(message: str) -> None:
    raise SystemExit(f"remote-evidence check failed: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def main() -> None:
    try:
        data = json.loads(EVIDENCE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot read evidence JSON: {exc}")

    require(data.get("schema") == "minvol.rc1_remote_audit.v1", "unexpected schema")

    candidate = data.get("candidate")
    workflow = data.get("hosted_workflow")
    fresh = data.get("fresh_clone")
    artifacts = data.get("transfer_artifacts")
    boundary = data.get("claim_boundary")
    for name, value in (
        ("candidate", candidate),
        ("hosted_workflow", workflow),
        ("fresh_clone", fresh),
        ("transfer_artifacts", artifacts),
        ("claim_boundary", boundary),
    ):
        require(isinstance(value, dict), f"{name} must be an object")

    commit = candidate.get("commit")
    require(isinstance(commit, str) and HEX40.fullmatch(commit) is not None, "invalid candidate commit")
    require(candidate.get("version") == "v1.0.0-rc1", "unexpected candidate version")
    require(candidate.get("branch") == "main", "candidate branch is not main")
    require(candidate.get("fresh_history_commit_count") == 5, "unexpected public-history count")
    repository = candidate.get("repository")
    require(repository == "https://github.com/swihart/minvol-degree3-contact-bound", "unexpected repository")
    require(candidate.get("repository_visibility_at_audit") == "private staging", "visibility boundary changed")

    run_id = workflow.get("run_id")
    run_url = workflow.get("run_url")
    require(isinstance(run_id, int) and run_id > 0, "invalid workflow run id")
    require(run_url == f"{repository}/actions/runs/{run_id}", "workflow URL and run id disagree")
    require(workflow.get("checked_out_commit") == commit, "workflow checked out the wrong commit")

    jobs = workflow.get("jobs")
    require(isinstance(jobs, list) and len(jobs) == 3, "expected exactly three hosted jobs")
    names = {job.get("name") for job in jobs if isinstance(job, dict)}
    require(names == EXPECTED_JOBS, "hosted job names do not match the workflow")
    for job in jobs:
        require(job.get("result") == "success", f"hosted job did not succeed: {job.get('name')}")
        require(job.get("required_markers_observed") is True, f"pass markers missing: {job.get('name')}")

    require(fresh.get("branch") == "main", "fresh clone branch is not main")
    require(fresh.get("head") == commit, "fresh clone HEAD differs from candidate")
    require(fresh.get("origin_main") == commit, "fresh clone origin/main differs from candidate")
    require(fresh.get("fresh_history_commit_count") == 5, "fresh clone history count differs")
    require(fresh.get("complete_language_replay") == "pass", "fresh-clone all-language replay did not pass")
    require(fresh.get("final_git_status_short_empty") is True, "fresh clone was not clean")
    require(fresh.get("bundle_records_complete_history") is True, "bundle did not record complete history")
    require(fresh.get("markdown_sources") == 22, "unexpected Markdown-source count")
    require(fresh.get("paired_reference_pdfs") == 22, "unexpected reference-PDF count")
    require(fresh.get("paired_rebuilt_pdfs") == 22, "unexpected rebuilt-PDF count")

    required_artifact_names = {"manifest", "main_bundle", "fresh_replay", "github_actions_logs"}
    require(set(artifacts) == required_artifact_names, "unexpected transfer-artifact set")
    for name, record in artifacts.items():
        require(isinstance(record, dict), f"artifact record is not an object: {name}")
        digest = record.get("sha256")
        require(isinstance(digest, str) and HEX64.fullmatch(digest) is not None, f"invalid SHA-256: {name}")
        require(isinstance(record.get("filename"), str) and record["filename"], f"missing filename: {name}")

    for key in (
        "external_mathematical_reproduction",
        "peer_review",
        "public_release",
        "immutable_tag",
        "meissner_extremality",
    ):
        require(boundary.get(key) is False, f"claim boundary was overstated: {key}")

    for path in DOCS_WITH_COMMIT_AND_RUN:
        text = path.read_text(encoding="utf-8")
        require(commit in text, f"candidate commit missing from {path.relative_to(ROOT)}")
        require(run_url in text, f"workflow URL missing from {path.relative_to(ROOT)}")

    all_markdown = "\n".join(
        path.read_text(encoding="utf-8")
        for path in ROOT.rglob("*.md")
        if ".git" not in path.parts and "build" not in path.parts
    )
    for phrase in STALE_PHRASES:
        require(phrase not in all_markdown, f"stale pre-remote wording remains: {phrase}")

    print(f"Candidate commit: {commit}")
    print(f"Hosted workflow: {run_url}")
    print("Hosted jobs: 3/3 success")
    print("Fresh-clone status: clean")
    print("MINVOL REMOTE-EVIDENCE CHECK: PASS")


if __name__ == "__main__":
    main()
