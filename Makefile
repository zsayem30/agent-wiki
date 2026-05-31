.PHONY: context lint tree scan timestamp report

context:
	python scripts/wiki/contextualize.py --role implementer

lint:
	python scripts/wiki/lint.py

tree:
	python scripts/wiki/build_tree.py

scan:
	python scripts/wiki/scan_changes.py

timestamp:
	python scripts/wiki/timestamp.py

report:
	python scripts/wiki/new_report.py project_status

