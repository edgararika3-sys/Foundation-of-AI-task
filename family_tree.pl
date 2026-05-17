% ============================================================
%  PROLOG FAMILY TREE — Task Three (c)
%  Family: The Anderson Family
%  Contains: grandparents, parents, children, grandchildren,
%            cousins, uncles, aunts
% ============================================================

% ------------------------------------------------------------
% FACTS — parent(Parent, Child)
% ------------------------------------------------------------

% Grandparents → Parents
parent(george_anderson, david_anderson).
parent(george_anderson, susan_anderson).
parent(mary_anderson,  david_anderson).
parent(mary_anderson,  susan_anderson).

parent(harold_baker,   linda_baker).
parent(harold_baker,   robert_baker).
parent(dorothy_baker,  linda_baker).
parent(dorothy_baker,  robert_baker).

% Parents → Children
parent(david_anderson, emma_anderson).
parent(david_anderson, james_anderson).
parent(linda_baker,    emma_anderson).   % Linda married David
parent(linda_baker,    james_anderson).

parent(robert_baker,   sophie_baker).
parent(robert_baker,   tom_baker).
parent(susan_anderson, sophie_baker).    % Susan married Robert
parent(susan_anderson, tom_baker).

% Children → Grandchildren
parent(emma_anderson,  lily_anderson).
parent(emma_anderson,  noah_anderson).
parent(james_anderson, oliver_anderson).

% ------------------------------------------------------------
% FACTS — male/female
% ------------------------------------------------------------
male(george_anderson).
male(harold_baker).
male(david_anderson).
male(robert_baker).
male(james_anderson).
male(tom_baker).
male(noah_anderson).
male(oliver_anderson).

female(mary_anderson).
female(dorothy_baker).
female(susan_anderson).
female(linda_baker).
female(emma_anderson).
female(sophie_baker).
female(lily_anderson).

% ------------------------------------------------------------
% RULES
% ------------------------------------------------------------

% father/mother
father(F, C) :- parent(F, C), male(F).
mother(M, C) :- parent(M, C), female(M).

% grandparent
grandparent(GP, GC) :-
    parent(GP, P),
    parent(P,  GC).

grandfather(GF, GC) :- grandparent(GF, GC), male(GF).
grandmother(GM, GC) :- grandparent(GM, GC), female(GM).

% grandchild
grandchild(GC, GP) :- grandparent(GP, GC).

% sibling (same parent, different person)
sibling(X, Y) :-
    parent(P, X),
    parent(P, Y),
    X \= Y.

brother(X, Y) :- sibling(X, Y), male(X).
sister(X,  Y) :- sibling(X, Y), female(X).

% uncle / aunt
uncle(U, C) :-
    parent(P, C),
    brother(U, P).

aunt(A, C) :-
    parent(P, C),
    sister(A, P).

% cousin
cousin(X, Y) :-
    parent(PX, X),
    parent(PY, Y),
    sibling(PX, PY).

% ancestor (recursive)
ancestor(A, D) :- parent(A, D).
ancestor(A, D) :- parent(A, X), ancestor(X, D).

% descendant
descendant(D, A) :- ancestor(A, D).

% ============================================================
%  SAMPLE QUERIES TO TRY IN THE PROLOG CONSOLE
% ============================================================
%
%  ?- grandparent(george_anderson, X).
%  ?- grandfather(harold_baker, X).
%  ?- grandmother(mary_anderson, X).
%  ?- uncle(U, sophie_baker).
%  ?- aunt(A, james_anderson).
%  ?- cousin(X, Y).
%  ?- ancestor(george_anderson, lily_anderson).
%  ?- descendant(X, george_anderson).
%  ?- sibling(david_anderson, susan_anderson).
%  ?- mother(M, emma_anderson).
%  ?- father(F, tom_baker).
%
% ============================================================
