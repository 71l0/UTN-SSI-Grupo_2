#!/usr/bin/env bash
# Ejecuta localmente las mismas verificaciones del pipeline.
# Uso: ./run_checks.sh secure|vulnerable
# Requisitos: pip install semgrep pip-audit   y   gitleaks en el PATH
set -u
TARGET="${1:-secure}"
fail=0
echo "=== 1/3 Secretos (Gitleaks) — $TARGET"
gitleaks detect --no-git --source "$TARGET" --redact -v || fail=1
echo; echo "=== 2/3 SAST (Semgrep) — $TARGET"
semgrep scan --config semgrep-rules.yml --error --metrics off "$TARGET" || fail=1
echo; echo "=== 3/3 SCA (pip-audit) — $TARGET"
pip-audit -r "$TARGET/requirements.txt" --strict || fail=1
echo
if [ $fail -eq 0 ]; then echo "✅ PIPELINE APROBADO"; else echo "❌ PIPELINE BLOQUEADO: corregir antes de desplegar"; fi
exit $fail
