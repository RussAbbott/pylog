/**<> The Zebra problem
 One version of the famous Zebra problem.
(All versions are structurally similar, but the names are often different.)

There are 5 houses in a row, each with a unique color.
Each house is occupied by a family of a unique nationality.
Each family has a pet, a favorite smoke, and a favorite drink.

Solution:

Houses:
  1. Norwegians(Kool, fox, water, yellow)
  2. Ukrainians(Chesterfield, horse, tea, blue)
  3. English(Old Gold, snails, milk, red)
  4. Spanish(Lucky, dog, juice, white)
  5. Japanese(Parliament, zebra, coffee, green)

  The Japanese own a zebra, and the Norwegians drink water.

*/

use_module(library(lists)).

is_a_subsequence_of([], _).
is_a_subsequence_of([Y|Ys], [Y|Xs]) :-
    is_a_subsequence_of(Ys, Xs).
is_a_subsequence_of([Y|Ys], [_|Xs]) :-
    is_a_subsequence_of([Y|Ys], Xs).

is_contiguous_in([X,Y], [X,Y|_]).
is_contiguous_in([X,Y],[_|L]):- is_contiguous_in([X,Y],L).

members([],_).
members([X|Xs], L):-
    member(X, L),
    members(Xs, L).

next_to_in(E1, E2, Es):-
    is_contiguous_in([E1,E2],Es);
    is_contiguous_in([E2,E1],Es).

/* house(nationality, smoke, pet, drink, color)*/
zebra_problem(Houses):-
    Houses = [house(_,_,_,_,_),house(_,_,_,_,_),house(_,_,_,_,_),house(_,_,_,_,_),house(_,_,_,_,_)],
    clue1(Houses),clue2(Houses),clue3(Houses),clue4(Houses),clue5(Houses),
    clue6(Houses),clue7(Houses),clue8(Houses),clue9(Houses),clue10(Houses),
    clue11(Houses),clue12(Houses),clue13(Houses),clue14(Houses),clue15(Houses).


/*1. The English live in the red house.*/
clue1(Houses):- member(house(english,_,_,_,red), Houses).
/*2. The Spanish have a dog.*/
clue2(Houses):- member(house(spanish,_,dog,_,_), Houses).
/*3. They drink coffee in the green house.*/
clue3(Houses):- member(house(_,_,_,coffee,green), Houses).
/*4. The Ukrainians drink tea.*/
clue4(Houses):- member(house(ukrainians,_,_,tea,_), Houses).
/*5. The green house is immediately to the right of the white house.*/
clue5(Houses):- is_contiguous_in([house(_,_,_,_,white), house(_,_,_,_,green)], Houses).
/*6. The Old Gold smokers have snails.*/
clue6(Houses):- member(house(_,'old gold',snails,_,_), Houses).
/*7. They smoke Kool in the yellow house.*/
clue7(Houses):- member(house(_,kool,_,_,yellow), Houses).
/*8. They drink milk in the middle house.*/
clue8([_,_,house(_,_,_,milk,_),_,_]).
/*9. The Norwegians live in the first house on the left.*/
clue9([house(norwegians,_,_,_,_)|_]).
/*10. The Chesterfield smokers live next to the fox.*/
clue10(Houses):- next_to_in(house(_,chesterfield,_,_,_), house(_,_,fox,_,_), Houses).
/*11. They smoke Kool in the house next to the horse.*/
clue11(Houses):- next_to_in(house(_,kool,_,_,_), house(_,_,horse,_,_), Houses).
/*12. The Lucky smokers drink juice.*/
clue12(Houses):- member(house(_,lucky,_,juice,_), Houses).
/*13. The Japanese smoke Parliament.*/
clue13(Houses):- member(house(japanese,parliament,_,_,_), Houses).
/*14. The Norwegians live next to the blue house.*/
clue14(Houses):- next_to_in(house(norwegians,_,_,_,_), house(_,_,_,_,blue), Houses).
/*Who has a zebra and who drinks water?*/
clue15(Houses):- members([house(_,_,zebra,_,_), house(_,_,_,water,_)], Houses).






