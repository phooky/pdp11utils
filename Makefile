
MACRO11=./macro11

all: pakdump.out

%.out: %.mac
	$(MACRO11) -o $@ -l $*.lst $<

