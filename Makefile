# make is actually pretty useful for helping keep things tidy.
#
# and years of practice have made 'make clean' part of my hind-brain.

clean:
	@find . -name '*~' -o -name '*.orig' -exec rm -f {} \;

distclean: clean
	@find . -name '*.pyc' -exec rm -f {} \;
