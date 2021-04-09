# Definitions of "Make Tasks" automating repetitive things like linting,
# minification, compilation, etc.
#
# To execute a task from this file, start a terminal, switch to the directory
# with this Makefile and run:
#
#   make <task-name>
#
# For example, `make server` will start a development server and `make css`
# will build production-ready CSS files from SASS sources.
#
# Unlike Gulp or Grunt, Make doesn't need any special JavaScript's runtime or
# plugins. If you can describe your task using a set of shell commands, you
# may use them as your task in Make as well.
#
STATIC_DIR=./app/frontend/static
CSS_DIR=$(STATIC_DIR)/css
SCSS_DIR=$(CSS_DIR)/src


PHONY: server

server:
	./waitforit.sh ${POSTGRES_HOST}:${POSTGRES_PORT} -- uvicorn app.main:app --host=0.0.0.0 --port=8000 --reload


# ***********
# *** CSS ***
# ***********

PHONY: css css-compile css-watch css-minify css-prefix

css-prefix:
	npx postcss --use autoprefixer --no-map --replace $(CSS_DIR)/**/*.css

css-minify:
	npx postcss --use cssnano --no-map --replace $(CSS_DIR)/**/*.css

css-watch:
	watchmedo shell-command --recursive --patterns="*.scss" --command="make css-compile" $(SCSS_DIR)

css-compile:
	sass --load-path=. $(SCSS_DIR):$(CSS_DIR)
	make css-prefix

css:
	make css-compile
	make css-prefix
	make css-minify


# ******************
# *** JavaScript ***
# ******************

PHONY: js js-compile js-watch js-lint

js:
	make js-lint
	make js-compile

js-compile:
	npx rollup --config

js-watch:
	npx rollup --config --watch

js-lint:
	npx eslint ./app/frontend/static/js/src
