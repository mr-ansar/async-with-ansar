# Author: Scott Woods <scott.18.ansar@gmail.com.com>
# MIT License
#
# Copyright (c) 2022
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# This repo needs the following;
# - python3 -m venv .env
# - source .env/bin/activate
# - pip install pyinstaller
# - pip install ansar-create
# - make build
#
# The repo is ready. Running a make at this point executes the final version
# of the demonstration.
# - make

SCRIPT_1 = db-query-interrupt db-query-stateless device-poll network-request-server query-request-poll-concurrent
SCRIPT_2 = db-query device_if hello-world query-request-poll-3-way query-request-poll

# Generate useful lists of build artefacts.
EXECUTABLES := $(SCRIPT_1) $(SCRIPT_2)
BUILD := $(EXECUTABLES:%=dist/%)
SPEC := $(EXECUTABLES:%=%.spec)

# The default target is to build.
all: run

# Turn a python script into an executable.
dist/% : %.py
	pyinstaller --onefile --log-level ERROR -p . $<

clean::
	-rm -rf build dist

# All the executables.
build: $(BUILD)

run: build
	PATH="${PWD}/dist:${PATH}" dist/query-request-poll-3-way --debug-level=DEBUG

clean::
	-rm -f $(SPEC)
