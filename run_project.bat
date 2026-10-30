@echo off
call venv\Scripts\activate
python ml\generate_dataset.py
python ml\train_rnn.py
python app.py
