# HANGMAN GAME For Command Line

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

At the start of the game the hangman is empty, so there is not head, body, arms and legs. For each wrong guess of the second player a part of the body is added in this order: head, body, left arm, right arm, left leg, right leg, left foot and right foot. At the end of the game, the guesser loses if all the part have been inserted, otherwise he wins.

## Additions to Hangman
