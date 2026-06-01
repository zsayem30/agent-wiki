.PHONY: context lint tree scan timestamp

context:
	python scripts/wiki/contextualize.py --role wiki-curator

lint:
	python scripts/wiki/lint.py

tree:
	python scripts/wiki/build_tree.py

scan:
	python scripts/wiki/scan_changes.py

timestamp:
	python scripts/wiki/timestamp.py
