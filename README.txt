Contains
_____________________________________________________________

README.txt - This file 

Angluin's Algorithm.py - This file contains the main implementation of Angluin's Algorithm.  It contains extensive commentary to guide you through the code.  It takes two files, a file of Training data from which to derive the Canonical Deterministic Finite State Machine, and a file of testing data with which to test the CDFSM on.  Two sample files are included.

LearningData.txt - This is the data that the CDFSM will learn from.  It is simply of lines of strings.  Each string is a sequence that will be fed into the algorithm, one line at a time.  The data is presented in the order frmo simplest to most complex, but it need not be.  The algorithm is robust enoug that it will derive the same CDFSM from any order the data is presented in, and with however many language-valid strings in the sample text (as long as it is at least sufficently long enough).  Though the numbers of what states may vary depending on the order the data is shown, the CDFSM will ultimately be unchanged, and any StateList and Translist can be mapped onto any other produced by the same data set, regardless of order.  There is only one ordering constraint, but this is due to python, not my code. If the Empty string is part fo the language, it cannot occur as the last item in the training set.  The reason for this is because when python reads the text file, it stops reading on the line of the last visible character, and will (understandably) disregard the (potentially infinite) blank lines that follow.

TestingData.txt - This is the data that we can test the CDFSM on (or have the CDFSM test for us against known data). It is identical in presentation format as the training data.

TestResults.txt - This is an example of the output produced by this program.  It contains information to recreate the CDFSM resulting from the training data, as well as the assessment of the Testing Data  The Training data used here was for the language of language of even numbers of 'A's and 'B's.  The testing data contains some lines in this language, and then the rest is composed of the training data for the language of odd numbers of 'A's and 'B's.  (I've had the algorithm run this and a few other regular languages, like the A^+ B^+ language, and the A^* language, and it works fine.)

_____________________________________________________________