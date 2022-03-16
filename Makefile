SHELL:=/bin/bash

.PHONY: clean

clean:
	find . -type d -name "__pycache__" | xargs rm -rf {};