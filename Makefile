
.PHONY: local-backup
local-backup:
	curl -X POST -H "Content-Type: application/json" \
	-d '{"id": "$(shell date +%Y%m%d%H%M%S)"}' \
	http://localhost:8080/v1/backups/filesystem

.PHONY: env-init ei env-activate ea
env-init ei:
	python -m venv .venv

env-activate ea:
	source .venv/bin/activate
