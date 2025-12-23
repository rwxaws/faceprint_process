alias r := run
alias rv := run-env

default:
    @just --list

run:
    uv run streamlit run main.py

run-env:
    uv run --env-file .env streamlit run main.py
