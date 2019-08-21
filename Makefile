all:
	@bin/hugo --ignoreCache

new:
	@read -p "Enter new page id (like new-page-id): " PAGE; \
	bin/hugo new blog/$$PAGE.md; \
	mv content/$$PAGE.md content/blog/$$PAGE.md; \
	vim content/blog/$$PAGE.md
