export LANG

GIT_HASH=${CIRCLE_SHA1}
PACKAGES_FOLDER=/usr/local/lib/python3.9/dist-packages

Pipfile.lock: Pipfile
	docker-compose run --rm --name helix_pipenv_helix_service_kenan dev sh -c "rm -f Pipfile.lock && pipenv lock --dev --clear"

.PHONY:devsetup
devsetup: ## one time setup for devs
	make update && \
	make up && \
	make setup-pre-commit && \
	make tests && \
	make up

.PHONY:devdocker
devdocker: ## Builds the docker for dev
	docker-compose build --parallel

.PHONY: run
run: ## runs Flask app
	docker-compose run --rm --name helix_pipenv_helix_service_kenan dev pipenv run flask run

.PHONY: up
up: ## starts docker containers
	docker-compose up --build -d && \
	echo "waiting for helix_service_kenan service to become healthy" && \
	while [ "`docker inspect --format {{.State.Health.Status}} dev`" != "healthy" ]; do printf "." && sleep 2; done && \
	echo ""
	echo "helix_service_kenan Service: http://localhost:5000/graphql"

.PHONY: down
down: ## stops docker containers
	docker-compose down --remove-orphans

.PHONY:update
update: Pipfile.lock setup-pre-commit  ## Updates all the packages using Pipfile
	docker-compose run --rm --name helix_pipenv_helix_service_kenan dev pipenv sync && \
	make devdocker && \
	make run-pre-commit && \
	echo "In PyCharm, do File -> Invalidate Caches/Restart to refresh" && \
	echo "If you encounter issues with remote sources being out of sync, click on the 'Remote Python' feature on" && \
	echo "the lower status bar and reselect the same interpreter and it will rebuild the remote source cache." && \
	echo "See this link for more details:" && \
	echo "https://intellij-support.jetbrains.com/hc/en-us/community/posts/205813579-Any-way-to-force-a-refresh-of-external-libraries-on-a-remote-interpreter-?page=2#community_comment_360002118020"


.DEFAULT_GOAL := help
.PHONY: help
help: ## Show this help.
	# from https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY:tests
tests: ## Runs all the tests
	docker-compose run --rm --name helix_service_kenan_tests dev pytest tests

.PHONY:shell
shell: up ## Brings up the bash shell in dev docker
	docker-compose run --rm --name helix_service_kenan_shell dev /bin/sh

.PHONY:clean-pre-commit
clean-pre-commit: ## removes pre-commit hook
	rm -f .git/hooks/pre-commit

.PHONY:setup-pre-commit
setup-pre-commit: Pipfile.lock
	cp ./pre-commit-hook ./.git/hooks/pre-commit

.PHONY:run-pre-commit
run-pre-commit: setup-pre-commit
	./.git/hooks/pre-commit pre_commit_all_files
