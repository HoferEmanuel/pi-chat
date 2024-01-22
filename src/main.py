from action_mngr import wait_for_name, get_action, shut_down
from audio_player import play_wav

try:

    play_wav("boot")
        
    while True:
        wait_for_name()
        action = get_action()

        print(Fore.BLUE + str(action))

        if action == "shutdown":
           break

    shut_down()
except KeyboardInterrupt:
    shut_down()
  
