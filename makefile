run: install
	python .\installer\rqams-helper.py
install:
	pip install -i https://pypi.douban.com/simple -e .
clean:
	if exist installer\build rmdir /s /q installer\build
	if exist installer\dist rmdir /s /q installer\dist
	if exist installer\Output rmdir /s /q installer\Output
build: clean install
	.\installer\build.cmd
release: clean install
	.\installer\build.cmd release
