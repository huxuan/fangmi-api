run:
	python run.py
req:
	pip install -r requirements.txt
deploy:
	service fangmi-api reload
clean:
	find . -name '*.pyc' -print0 | xargs -0 rm -f
	find . -name '*.swp' -print0 | xargs -0 rm -f
	-@sudo rm -rf whoosh_index
permission:
	chown -R www-data.www-data .
