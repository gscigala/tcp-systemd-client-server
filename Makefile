PREFIX ?= /usr/local
TASK_DONE = echo -e "\n✓ $@ done\n"
# files that need mode 755
EXEC_SRC=src
BIN_DIR=tcp-systemd-client-server

all:
	@echo "usage: make install"
	@echo "       make reinstall"
	@echo "       make uninstall"

help:
	$(MAKE) all
	@$(TASK_DONE)

install:
	mkdir -p $(PREFIX)/share/$(BIN_DIR)	
	mkdir -p $(PREFIX)/bin/$(BIN_DIR)
	install src/logging.conf $(PREFIX)/share/$(BIN_DIR)/logging.conf
	install src/message.py $(PREFIX)/bin/$(BIN_DIR)/message.py
	install src/tcp-client.py $(PREFIX)/bin/$(BIN_DIR)/tcp-client.py
	install src/tcp-server.py $(PREFIX)/bin/$(BIN_DIR)/tcp-server.py
	@$(TASK_DONE)

uninstall:
	test -d $(PREFIX)/bin/$(BIN_DIR) && \
	cd $(PREFIX)/bin && \
	rm -rf $(BIN_DIR) \
	test -d $(PREFIX)/share/$(BIN_DIR) && \
	cd $(PREFIX)/share && \
	rm -rf $(BIN_DIR)
	@$(TASK_DONE)

reinstall:
	$(MAKE) uninstall && \
	$(MAKE) install
	@$(TASK_DONE)
