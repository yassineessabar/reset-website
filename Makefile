PORT ?= 8768
PY ?= python3

.PHONY: serve pages images check

## serve: run the site locally at http://localhost:$(PORT)
serve:
	$(PY) -m http.server $(PORT) -d public

## pages: rebuild the generated pages from index.html and scripts/content (idempotent)
pages:
	$(PY) scripts/footer.py
	$(PY) scripts/app_section.py
	$(PY) scripts/build_pages.py
	$(PY) scripts/build_business.py
	$(PY) scripts/seo.py
	$(PY) scripts/check_links.py

## images: rebuild the illustrations and the bright step / More ways photos
images:
	$(PY) scripts/build_illustrations.py
	$(PY) scripts/build_bright_photos.py

## check: every referenced file exists, no unused assets
check:
	$(PY) scripts/check_links.py
