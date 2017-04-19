.DEFAULT_GOAL := test

FILES :=            \
    IDB2.log     \
    app/models.py      \
    app/TestMagic.out \
    app/TestMagic.py  \
    .travis.yml     \
    IDB2.html    \
    IDB2.pdf		\

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

IDB2.html: app/testmodels.py
	pydoc3 -w app/testmodels.py
	mv testmodels.html IDB2.html
	rm -f testmodels.html

IDB2.log:
	git log > IDB2.log

TestMagic.tmp: app/testmodels.py .pylintrc app/models.py 
	-$(PYLINT) app/models.py
	-$(COVERAGE) run    --branch --include=app/TestMagic.py app/TestMagic.py > app/TestMagic.out 2>&1
	-$(COVERAGE) report -m app/TestMagic.py >> app/TestMagic.out
	cat app/TestMagic.out

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
	rm -f  IDB1.html
	rm -f  IDB1.log
	rm -f  IDB2.html
	rm -f  IDB2.log
	rm -f  TestMagic.tmp
	rm -rf __pycache__\

config:
	git config -l

format:
	$(AUTOPEP8) -i app/models.py
	$(AUTOPEP8) -i app/TestMagic.py

status:
	make clean
	@echo
	git branch
	git remote -v
	git status

test: TestMagic.tmp
	ls -al
	make check

logtml: IDB2.html IDB2.log 

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

