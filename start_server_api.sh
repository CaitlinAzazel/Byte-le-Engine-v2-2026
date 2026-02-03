source .venv/bin/activate
rm *.db*
uvicorn server.main:app --reload
