#!/usr/bin/env python3
"""RECONCILE-1 domain importer. Checks out a domain's ONLY_R35L31 files
verbatim from origin/claude/cvln-academy-production-r35l31 into the current
worktree (must already be on reconcile/canonical-main-r35l31-20260914),
verifies count + Python syntax + local-import references, and appends to
the tracker. Does NOT commit -- the caller commits after reviewing output.
"""
import json
import subprocess
import sys
import os
import re
import ast

R35 = "origin/claude/cvln-academy-production-r35l31"
TRACKER = "docs/reconciliation/import_tracker.tsv"
CLASSIFICATION = "docs/reconciliation/domain_classification.json"


def sh(*args, check=True):
    r = subprocess.run(args, capture_output=True, text=True)
    if check and r.returncode != 0:
        raise RuntimeError(f"cmd failed: {args}\n{r.stdout}\n{r.stderr}")
    return r.stdout


def load_domain_files(domain):
    with open(CLASSIFICATION) as f:
        data = json.load(f)
    return data[domain]["ONLY_R35L31"]


def all_repo_py_modules():
    """Top-level package/module names under backend/ currently in the worktree."""
    out = sh("git", "ls-files", "backend")
    tops = set()
    for line in out.splitlines():
        rel = line[len("backend/") :] if line.startswith("backend/") else line
        if not rel:
            continue
        tops.add(rel.split("/")[0].removesuffix(".py"))
    return tops


def local_import_targets(pyfile_content):
    """Best-effort: local (non-stdlib, non-3rd-party) module names referenced."""
    targets = set()
    try:
        tree = ast.parse(pyfile_content)
    except SyntaxError:
        return targets, "SYNTAX_ERROR"
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if node.module and node.level == 0:
                targets.add(node.module.split(".")[0])
        elif isinstance(node, ast.Import):
            for alias in node.names:
                targets.add(alias.name.split(".")[0])
    return targets, None


def main():
    domain = sys.argv[1]
    files = load_domain_files(domain)
    print(f"=== {domain}: {len(files)} fichiers attendus (ONLY_R35L31) ===")

    # 1) checkout each file verbatim from r35l31
    for i in range(0, len(files), 200):
        batch = files[i : i + 200]
        sh("git", "checkout", R35, "--", *batch)
    staged = sh("git", "diff", "--cached", "--name-only").splitlines()
    staged_set = set(staged)
    missing = [f for f in files if f not in staged_set]
    extra = [f for f in staged if f not in set(files)]
    print(f"stagé réellement: {len(staged)} | attendu manquant: {len(missing)} | inattendu en trop: {len(extra)}")
    if missing:
        print("MANQUANTS:", missing[:20])
    if extra:
        print("EN TROP (ne devrait pas arriver):", extra[:20])

    # 2) py_compile / ast syntax check on new .py files
    py_files = [f for f in files if f.endswith(".py")]
    syntax_errors = []
    broken_refs = []
    known_top_pkgs = all_repo_py_modules()

    for pf in py_files:
        if not os.path.exists(pf):
            continue
        with open(pf, encoding="utf-8") as fh:
            content = fh.read()
        targets, err = local_import_targets(content)
        if err:
            syntax_errors.append(pf)
            continue
        # only flag targets that look like same-repo backend packages we know about
        # (api, services, certification, wallet, skills, fms_import, fms_lineage,
        #  klt_canonical, kor_canonical, frk_canonical, fms_canonical, master_canonical,
        #  canonical_common, qualification, template_engine, commerce, payments)
        backend_pkg_names = {
            "api", "services", "certification", "wallet", "skills", "fms_import",
            "fms_lineage", "klt_canonical", "kor_canonical", "frk_canonical",
            "fms_canonical", "master_canonical", "canonical_common", "qualification",
            "template_engine", "commerce", "payments",
        }
        for t in targets:
            if t in backend_pkg_names and t not in known_top_pkgs:
                broken_refs.append((pf, t))

    if syntax_errors:
        print(f"ERREURS DE SYNTAXE ({len(syntax_errors)}):", syntax_errors[:20])
    if broken_refs:
        print(f"REFERENCES VERS PACKAGE ABSENT ({len(broken_refs)}):")
        for pf, t in broken_refs[:40]:
            print(f"  {pf} -> import de '{t}' (package non present dans le worktree actuel)")

    print(f"\nRESUME {domain}: importes={len(staged)-len(missing) if staged else 0} "
          f"syntax_errors={len(syntax_errors)} broken_refs={len(set(p for p,_ in broken_refs))}")


if __name__ == "__main__":
    main()
