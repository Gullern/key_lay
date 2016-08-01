DIRS=

CLEAN_DIRS=$(addsuffix .clean,$(DIRS))
VCLEAN_DIRS=$(addsuffix .vclean,$(DIRS))

all:

init: pip install -r requirements.txt

gen_req: pipreqs .

commit:
	git commit
	git push -u origin master

$(DIRS):
	$(MAKE) -C $(basename $@) all

clean: $(CLEAN_DIRS)

vclean: $(VCLEAN_DIRS)

$(CLEAN_DIRS):
	$(MAKE) -C $(basename $@) clean

$(VCLEAN_DIRS):
	$(MAKE) -C $(basename $@) vclean

.PHONY: all clean vclean $(DIRS) $(CLEAN_DIRS) $(VCLEAN_DIRS)
