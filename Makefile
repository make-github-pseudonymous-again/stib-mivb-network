.PHONY: diagnostic clean nuke

raw.json: code/scrape.py
	mkdir -p data
	python $< > $@

data.json: raw.json code/curate.py
	python > $@ < $^

diagnostic:
	python code/diagnostic.py < raw.json

clean:
	rm -rf raw.json data.json

nuke: clean
	rm -rf data
