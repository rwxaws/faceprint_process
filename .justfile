alias r := run
alias rh := run-headless
alias rv := run-env

default:
    @just --list

run:
    uv run streamlit run main.py

run-headless:
    uv run streamlit run --server.headless 1 main.py

run-env:
    uv run --env-file .env streamlit run main.py
