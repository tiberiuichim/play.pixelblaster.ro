content:
	python ./split_content.py

build:
	lektor build --output-path ./build

dist-clean:
	rm -rf content/ build/

all:
	.dist-clean
