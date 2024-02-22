run_example:
	@echo "Running example"
	@python3 app/example.py
	@echo "Done"

build_and_run_docker:
	@echo "Building Docker image"
	@docker build -t myapp .
	@echo "Running Docker container"
	@docker run myapp
	@echo "Done"
