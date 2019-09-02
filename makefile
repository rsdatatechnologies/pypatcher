install:
	pip3 install -r requirements.txt
	sudo chmod +x pypatcher.py
	cp pypatcher.py /usr/local/bin/pypatcher

example-simple:
	cat example/simple/redis.yaml | pypatcher -p example/simple/redis_prod_patch.yaml > example/simple/redis_production.yaml

example-project-dev:
	$(call patch,example/project/config_template,example/project/patches/dev,example/project/config)

example-project-prod:
	$(call patch,example/project/config_template,example/project/patches/prod,example/project/config)

patch = \
	for f in $$(ls $(1)/*); do \
		filename=$$(echo $${f}| cut -d'/' -f 4) ; \
		cat $$f | pypatcher -p $(2)/$$filename > $(3)/$$filename; \
	done;
