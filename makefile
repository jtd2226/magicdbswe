.DEFAULT_GOAL := test

FILES :=            \
    Magic.log     \
    models.py      \
    TestMagic.out \
    TestMagic.py  \
    .travis.yml     \
    #models.html    \

ifeq ($(shell uname), Darwin)          # Apple
    PYTHON   := python3.5
    PIP      := pip3.5
    PYLINT   := pylint
    COVERAGE := coverage-3.5
    PYDOC    := pydoc3.5
    AUTOPEP8 := autopep8
else ifeq ($(CI), true)                # Travis CI
    PYTHON   := python3.5
    PIP      := pip3.5
    PYLINT   := pylint
    COVERAGE := coverage-3.5
    PYDOC    := pydoc3.5
    AUTOPEP8 := autopep8
else ifeq ($(shell uname -p), unknown) # Docker
    PYTHON   := python3.5
    PIP      := pip3.5
    PYLINT   := pylint
    COVERAGE := coverage-3.5
    PYDOC    := pydoc3.5
    AUTOPEP8 := autopep8
else                                   # UTCS
    PYTHON   := python3
    PIP      := pip3
    PYLINT   := pylint3
    COVERAGE := coverage-3.5
    PYDOC    := pydoc3.5
    AUTOPEP8 := autopep8
endif

.pylintrc:
	$(PYLINT) --disable=locally-disabled --reports=no --generate-rcfile > $@

Magic.html: models.py
	pydoc3 -w models

Magic.log:
	git log > Magic.log

TestMagic.tmp: models.py TestMagic.py .pylintrc
	-$(PYLINT) TestMagic.py
	-$(COVERAGE) run    --branch TestMagic.py >  TestMagic.tmp 2>&1
	-$(COVERAGE) report -m                      >> TestMagic.tmp
	cat TestMagic.tmp

check:
	@not_found=0;                                 \
    for i in $(FILES);                            \
    do                                            \
        if [ -e $$i ];                            \
        then                                      \
            echo "$$i found";                     \
        else                                      \
            echo "$$i NOT FOUND";                 \
            not_found=`expr "$$not_found" + "1"`; \
        fi                                        \
    done;                                         \
    if [ $$not_found -ne 0 ];                     \
    then                                          \
        echo "$$not_found failures";              \
        exit 1;                                   \
    fi;                                           \
    echo "success";

clean:
	rm -f  .coverage
	rm -f  .pylintrc
	rm -f  *.pyc
	rm -f  models.html
	rm -f  Magic.log
	rm -f  TestMagic.tmp
	rm -rf __pycache__\

config:
	git config -l

format:
	$(AUTOPEP8) -i models.py
	$(AUTOPEP8) -i TestMagic.py

status:
	make clean
	@echo
	git branch
	git remote -v
	git status

test: Magic.html Magic.log #testmagic
	ls -al
	make check

logtml: Magic.html Magic.log

versions:
	which make
	make --version
	@echo
	which git
	git --version
	@echo
	which $(PYTHON)
	$(PYTHON) --version
	@echo
	which $(PIP)
	$(PIP) --version
	@echo
	which $(PYLINT)
	$(PYLINT) --version
	@echo
	which $(COVERAGE)
	$(COVERAGE) --version
	@echo
	-which $(PYDOC)
	-$(PYDOC) --version
	@echo
	which $(AUTOPEP8)
	$(AUTOPEP8) --version
	@echo
	$(PIP) list
