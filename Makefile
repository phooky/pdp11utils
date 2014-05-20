
MACRO11=./macro11
OBJ_DUMPER=./objdumper.py

all: pakdump.out pakdump.simh

%.simh: %.out
	$(OBJ_DUMPER) $< -s $@

%.out: %.mac
	$(MACRO11) -o $@ -l $*.lst $<

