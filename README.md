# Chatbot Countries
## Introduction
Using [Rasa 3.0](https://rasa.com/docs/rasa/) to create a customized, and user friendly AI bot that can help with countries.
you can ask things like:
- Show me countries around the world.
- What do you know about Greece?
- what is the population of Australia?
- Tell me the capital of Japan.

It can Handle different stories, variations, and case sensitive words.
example:
- -Input-> Tell me the capital of USA.
- -Bot-> Washington, D.C. is the capital of USA. 
- -Input-> what about its population?
- -Bot-> There is 32.82 crores in USA.

## Run chatbot
To run chatbot on your system you need to install rasa 3.0 on your virtual environment (anaconda)
following this link to install rasa on your local drive: [youtube](https://www.youtube.com/watch?v=GlR60CvTh8A) or [Rasa documentation](https://rasa.com/docs/rasa/installation)

after installation:
1. Open your conda virtual env for rasa in terminal.
2. Clone this repo to your project directory
3. Open the first terminal, and run:
    - -> rasa train
4. Open new terminal with rasa virtual env to run actions server, make sure you are in the project directory, and run: 
    - -> rasa actions run
5. Get back to the first terminal, and run:
    - -> rasa shell
6. From here you are good to go with the chatbot. **Have fun!**

Note: for a more interactive way, and to get to share chatbot link over the network see [rasa x](https://rasa.com/docs/rasa-x/installation-and-setup/installation-guide).

## Bot example
Here is an example for a conversation driven through different turns.

<img src="https://github.com/hazemhosny/Chatbot_Countries/blob/main/BotExample.png" alt="BotExample" width="850"/>
