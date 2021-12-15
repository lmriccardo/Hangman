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

## Game Mode
As we have already said, there are four game mode: E, M, H and VH. Let's explore them.

|           | N. Round | Time x Round | Min Word Len | Max Word Len | Penalty | Min Hint N. | Max Hint N. | Hint Penalty |
|-----------|----------|--------------|--------------|--------------|---------|-------------|-------------|--------------|
| Easy      |    10    |    60 sec    |       5      |       7      |    1    |      3      |      5      |       0      |
| Medium    |    10    |    300 sec   |       7      |       9      |    1    |      2      |      4      |       0      |
| Hard      |    10    |    600 sec   |       9      |      11      |    1    |      1      |      3      |       0      |
| Very Hard |    10    |   1200 sec   |      11      |      18      |    2    |      1      |      3      |       1      |

