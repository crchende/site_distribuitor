# Oprire rulari anterioare in screen-uri
killall gunicorn
sleep 1
screen -X -S apioferte quit
sleep 0.5
screen -X -S chocodist quit
sleep 0.5

# Pornire server RESTAPI oferte
screen -dmS apioferte
sleep 0.1
screen -S apioferte -X stuff 'source ./activeaza_venv\n'
sleep 0.2
screen -S apioferte -X stuff 'gunicorn apioferte:create_app -b 127.0.0.1:5001\n'
sleep 0.1

# ================================
screen -dmS chocodist
sleep 0.1
screen -S chocodist -X stuff 'source ./activeaza_venv\n'
sleep 0.2
#screen -S chocodist -X stuff 'flask --app chocodist run --reload\n'
screen -S chocodist -X stuff 'gunicorn chocodist:app -b 127.0.0.1:8002\n'
sleep 0.2
screen -ls
echo -e Use:"\n"'    screen -r chocodist'"\n"to attach to the screen in which the chocodist app is running!
echo -e '    screen -r apioferte'"\n"to attach to the screen in which the rest api server is running!"\n"