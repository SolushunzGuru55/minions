CURRENT_DIR = $(shell pwd)
STACK_NAME = my-stack
JSON_FILE = multiple.json

create_json:
	python template_maker.py > $(JSON_FILE)

create_stack: create_json
	aws cloudformation create-stack --stack-name $(STACK_NAME) --template-body file://$(CURRENT_DIR)/$(JSON_FILE)

delete_stack:
	aws cloudformation delete-stack --stack-name $(STACK_NAME)

deploy: create_stack

clean:
	rm $(JSON_FILE)
