IMAGE=rc4me

build-docker:
	docker build -t $(IMAGE):latest .

bash: build-docker
	docker run -it $(IMAGE):latest bash

