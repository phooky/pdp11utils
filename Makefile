DIRS=./macro11
MACRO11=./macro11/macro11
OBJ_DUMPER=./objdumper.py

OBJS=pakdump.out pakdump.simh
all: $(OBJS)

.PHONY: subdirs $(DIRS)
     
subdirs: $(DIRS)
   
$(DIRS):
	$(MAKE) -C $@
     
%.simh: %.out subdirs
	$(OBJ_DUMPER) $< -s $@

%.out: %.mac
	$(MACRO11) -o $@ -l $*.lst $<

clean:
	rm -f $(OBJS)
