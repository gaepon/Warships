Requires Pyside6 to launch with GUI

command-line launch :
    >$ python3 main.py

options :
    --noShow : The game will not use ant print or matplotlib graph. 
               Only one print at the end to indicate the nombre of turns
    
    --aiOnly : Only plays with AIs, the first AI will always target the same coordinates

    --RandomAI, --HeuristicAI, --ProbabilisticAI : Only used with --aiOnly, choose the AI that will play

To launch with GUI :
    >$ python3 mainGUI.py
The game is only playable between two human players if you use the GUI

To launch statistic tests :
    >$ python3 projectStats.py