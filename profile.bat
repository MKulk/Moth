REM python -m cProfile CS.py >> out.txt
python -m cProfile -o program.prof CS.py
snakeviz -p 8088 program.prof