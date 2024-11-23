setup-env:
	@echo "Setting up backend/.env with default values. You can override them now."
	@touch backend/.env
	@rm -f backend/.env # Ensure no duplicate appends
	@for var in "FLASK_APP=app.main" \
	            "FLASK_ENV=development" \
	            "CLIENT_ID=some_id" \
	            "CLIENT_SECRET=some_secret" \
	            "REFRESH_TOKEN=some_token" \
	            "REDIRECT_URI=http://localhost:5000/callback" \
	            "DATABASE_URL=sqlite:///reddit_data.db" \
	            "OPENAI_API_KEY=sk-proj-etcetcetc" \
	            "OPENAI_API_PROJECT_ID=proj_etc" \
	            "NODE_ENV=development"; do \
		key=$$(echo $$var | cut -d= -f1); \
		default_value=$$(echo $$var | cut -d= -f2-); \
		read -p "$$key (default: $$default_value): " value; \
		if [ -z "$$value" ]; then \
			value=$$default_value; \
		fi; \
		echo "$$key=$$value" >> backend/.env; \
	done
	@echo ".env file created at backend/.env"
	
build:
	docker compose run frontend npm i
	docker compose up --build

up:
	docker compose up