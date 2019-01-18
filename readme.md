## Running Project
# Localhost
```pipenv shell
flask run```

or: 

```pipenv run flask run```

# Over Local WiFi
```pipenv shell```
```flask run --host=0.0.0.0```
Find your local with ```hostname -I``` on Linux
then go to <ip>:5000
Example:
10.0.1.29:5000


## To Do Before Publishing:
(Hardest to easiest)
- [X] Make money by adjacency (team members)
- [X] Switch to postgresql/deploy to heroku
- [X] Refactor code to properly use rooms
- [X] Add more feedback to move previewing, red when unpurchasable square.
- [X] Clean up any UI missteps
- [X] Show how much a square costs to buy
- [X] Fix Lobby Disconnects
- [X] Fix global error messages
- [X] Split teams up when players lose (not just disconnect)
- [X] Disconnect During Turn
- [X] Fix Broke Server
- [X] If player wins because opponent disconnects, immediate response.

## Fun Features:
- [ ] Create tutorial
- [ ] Create matchmaking System
- [ ] Customizable Board Sizes/Game Rules
- [ ] Redo color palatte
- [ ] Add interesting terrain squares: black unbuyable squares, double money squares, etc.
- [X] Mobile Optimize
- [X] Restyle game

