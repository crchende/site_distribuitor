screen -dmS chocodist
screen -S chocodist -X stuff 'source ./activeaza_venv\n'
#screen -S chocodist -X stuff 'flask --app chocodist run --reload\n'
screen -S chocodist -X stuff 'gunicorn chocodist:app -b 127.0.0.1:8002\n'
screen -ls
echo -e Use:"\n"'    screen -r chocodist'"\n"to attach to the screen in which the chocodist app is running! 