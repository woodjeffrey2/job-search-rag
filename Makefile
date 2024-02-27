
.PHONY: local-backup
local-backup:
	curl -X POST -H "Content-Type: application/json" \
	-d '{"id": "$(shell date +%Y%m%d%H%M%S)"}' \
	http://localhost:8080/v1/backups/filesystem

init-env ie:
	source .venv/bin/activate
