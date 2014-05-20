
MACRO11=./macro11
OBJ_DUMPER=./objdumper.py

OBJS=pakdump.out pakdump.simh
all: $(OBJS)

%.simh: %.out
	$(OBJ_DUMPER) $< -s $@

%.out: %.mac
	$(MACRO11) -o $@ -l $*.lst $<

clean:
	rm -f $(OBJS)
