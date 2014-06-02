DIRS=./macro11
MACRO11=./macro11/macro11
OBJ_DUMPER=./objdumper.py

OBJS=pakdmp.lda 
all: $(OBJS)

.PHONY: subdirs $(DIRS)
     
subdirs: $(DIRS)
   
$(DIRS):
	$(MAKE) -C $@
     
%.simh: %.out subdirs
	$(OBJ_DUMPER) $< -s $@

%.lda: %.mac
	python simh.py --send $< --do "MACRO/LIST:$*.LST $*" --do "LINK/LDA $*" --recv $*.LST --recv $@

clean:
	rm -f $(OBJS)
