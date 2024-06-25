SHELL:=/bin/bash
VERSION=0x03

FTPUSER ?=joshc

TST_FILES_ALL := $(wildcard tests/Test*.py)
TST_FILES_LOCAL := $(filter-out tests/TestHIL*, $(TST_FILES_ALL))

.PHONY: test
test:
	@source venv/bin/activate && pytest --capture=tee-sys -vv $(TST_FILES_LOCAL)

.PHONY: test_HIL
test_HIL:
	@source venv/bin/activate && pytest --capture=tee-sys -vv tests/TestHIL*

.PHONY: test_all
test_all:
	@source venv/bin/activate && pytest --capture=tee-sys -vv $(TST_FILES_ALL)

.PHONY: update_drops
update_drops:
	@cd drops && pip install --editable ..

.PHONY: run_test_server
run_test_server:
	@python3 tests/testServer.py

.PHONY: transfer_working_files
transfer_working_files:
	rsync -zvaP Makefile setup.py tests drops $(FTPUSER)@psbuild-rhel7:~/DoDRobotCode/

.PHONY: sync
sync:
	rsync -zvaP --exclude-from='.gitignore' ../DropletDispensingRobot/ psbuild-rhel7:~/DoDRobotCode/
