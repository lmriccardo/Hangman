# HANGMAN GAME For Command Line

This game is created using Python with the module curses

## Introduction
The Hangman game is a very old game in which there are two players and two respective role (I suppose): the **Conductor** and the **Guesser**. The first one must thinks at one word (hard or simple) to be shown to the second one, which goal is to guess that word. That is, the conductor write in a board only the first letter of the chosen word, while all the others are hidden and indicated with a simple underscore symbol. That means the guesser knows both the first letter and the length of the puzzle. Finally, in addition to the word displayed on the board, is displayed also the hangman like that

<pre>
-------------\
=============
|█          |
|█          O
|█         /|\
|█        _/ \_
|█
|█
|█
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
###################
</pre>

At the start of the game the hangman is empty, so there is no head, body, arms and legs. For each wrong guess of the second player a part of the body is added in this order: head, body, left arm, right arm, left leg, right leg, left foot and right foot. At the end of the game, the guesser loses if all the part have been inserted, otherwise he wins.

## Additions to Hangman
In this version of the game I did some additions to the original one. The first, and the main one, is that the user (who play the role of the guesser) can now choose with which difficulty he wants to play. There are four main difficulty: *Easy* (E), *Medium* (M), *Hard* (H) and *Very Hard* (VH, the last one is very hard). In the following section we are gonna explore each of them. In summary, the main differences between all the difficulty are regarding:

1. the minimum and the maximum length of the word that the user has to guess;
2. which letters of the words are already shown;
3. the number of hints the user has for each round;
4. the amount of time the user has to finish one round;
5. the penalty for each wrong try (in a single round);
6. the penalty for each used hint (in a single round, but it affects the final total score).

Note that, the last one is valid only for the Very Hard mode, since in a different mode the user has no penalty for have used a hint. Also, the 5-th difference change only in the VH-mode in fact, while in all the other cases only a single part of the body is added if the user has a wrong guess, in this difficulty for a single error two part of body are inserted (head and body, then all the arms, then all the legs and, finally, the feet).

Obviously, there are more additions. The second one is that there is a precise number of round (10) for each game, and the user needs to pass correct all of them in order to achieve the maximum total score. Note that, the score is expressed in percentage so, a totally correct round will give the reward of a 100%. This means, that the maximum total score is 100%. In general, the total score is the sum of the score for each round divided by the total number of round. 

Finally, other additions are:
+ the score;
+ the countdown timer for each round;
+ the hints (they are not in the original game);
+ higher the difficulty, more letter are already shown (in the original only the first);

> Note (HINT): using an hint means showing the letter where the user has currently the cursor

## Game Modes
As we have already said, there are four game mode: E, M, H and VH. Let's explore them.

|           | N. Round | Time x Round | Min Word Len | Max Word Len | Penalty | Min Hint N. | Max Hint N. | Hint Penalty |
|-----------|----------|--------------|--------------|--------------|---------|-------------|-------------|--------------|
| Easy      |    10    |    60 sec    |       5      |       7      |    1    |      3      |      5      |       0      |
| Medium    |    10    |    300 sec   |       7      |       9      |    1    |      2      |      4      |       0      |
| Hard      |    10    |    600 sec   |       9      |      11      |    1    |      1      |      3      |       0      |
| Very Hard |    10    |   1200 sec   |      11      |      18      |    2    |      1      |      3      |       1      |

> Note (HINT PENALTY): except for the first three modes, the VH-mode has the column _Hint Penalty_ set to 1. What does It mean? It means that at the end of the round the total score would be 0 if the user has lost, otherwise is the 100 - (word_len / (max_hint * 100)) * number_used_hints * hint_penalty. So, if *Hint penalty* is 0 then the score will remain the same (either 100 or 0). 

There is also another difference between the difficulty:
+ E Mode: only the first letter is shown at the start
+ M Mode: both the first and the last one letters are yet shown
+ H and VH Mode: first, middle and last letters are yet shown


## Requirements
We have some requirements:
+ art==5.3 (for ASCII ART)
+ pydub==0.25.1 (in order to play the music)
+ simpleaudio==1.0.4 (support for pydub)
+ curses (already installed in Unix/MacOS)

All of them are installable via pip using <code>pip install name==ver</code>, or directly using the requirements.txt file <code>pip install -r requirements.txt</code>. If you are using Linux and pip is not available then use <code>python3 -m pip install ...</code>, otherwise first install pip using <code>sudo apt-get install -y python3-pip</code> and then use the previous method. 

Some external requirements:
+ Linux/MaxOS (suggested, no need to install curses and colors may don't work);
+ install ffmpeg (to play the bkg music)
+ use Python 3.9 or above (**MANDATORY**)

### Install curses on Windows
Sadly, curses is not a module of the standard library of Python in Windows. In order to install it, you need to install NCurses and you can do it from [here](https://invisible-island.net/ncurses/). Otherwise, you can try to install from MinGW: look at [this](https://e-l.unifi.it/pluginfile.php/805205/mod_resource/content/0/ncurses%20installation%20-%20en.pdf). However, It really suggested to used a Unix-based OS.

### Install ffmpeg
In MacOS, it is really simple, just open a terminal and use <code>sudo brew install ffmpeg</code>. Otherwise, if you are in Linux first update the repo <code>sudo apt-get update</code> and then install the package <code>sudo apt-get install -y ffmpeg</code>. In windows, please search over the internet (I'm sorry bro).


## Run the game
There are two ways to download this game. The first one is through pip module. Essentially, after done <code>pip install hangman</code>, **PLEASE MAKE SURE YOU ARE IN A FULL SCREEN TERMINAL** you can run it with <code>python[ver] hangman</code>, where [ver] is the current version of python you are using to run the game. Another suggestion, if I can, is to create a python virtual environment, before running the game. It is very simple:

1. <code>python[ver] -m venv venv_name</code>
2. <code>source venv_name/bin/activate</code>
3. <code>pip install hangman</code>
4. <code>python hangman</code>

In Windows the second point change and become <code>.\venv_name\Scripts\activate</code>. Be careful, this may don't work and return the error *cannot be loaded because the execution of scripts is disabled on this system*. In this situation there are two ways to solve the problem (both changing policy restriction). Open your windows PowersShell in the current folder where you want to execute the game and write one of the two commands:

1. <code>Set-ExecutionPolicy Unrestricted -Scope Process</code>
2. <code>Set-ExecutionPolicy Unrestricted -Force</code>

the main difference is that the first one is regard the current process (so, the current PowerShell), while the second one is for the entire system.

The second method to download the game is through git. Just do the following steps:

1. <code>git clone -b cli_hangman https://github.com/lmriccardo/Hangman.git </code>
2. <code>cd Hangman</code>
3. <code>Create the virtual env and activate</code>
4. <code>pip install -r requirements.txt</code>
5. <code>python -m src.hangman</code>


## The output
After executing the game the conductor will introduce you to the Hangman game. When it finished to talk, the game will ask you with which difficulty you wanna play.

![](https://i.imgur.com/s7zZNQh.png)

the user can choose the difficulty simply moving with the arrows and then press ENTER. Once the user has chosen the difficulty, the game can start. Instead of displaying the difficulty question, inside the Hangman Game windows there are 4 sections. The first one (or the upper left) contains the hangman and the word the user has to guess. The botton left section is a logging window in which every action of the user is logged. The upper right mini-window display the game settings. Finally, the bottom right section display the game status. In addition, the title of the game window has changed displaying not only the original title but also the difficulty, some actions (1 to use hint and CTRL + c to quit the game) and finally the timer (on the right side). 

![](https://imgur.com/cYASZsQ.png)

The user can insert the letter that wants to try using the corresponding key on the keyboard. At the end of each round the user can wait 5 seconds before the next round start.