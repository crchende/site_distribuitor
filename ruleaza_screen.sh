screen -dmS chocodist
screen -S chocodist -X stuff 'source ./activeaza_venv\n'
screen -S chocodist -X stuff 'flask --app chocodist run --reload\n'
screen -ls