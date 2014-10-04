#An irc bot for the denizens of ##deutsch

##Usage
NB the space for general tranlsation:

    you: ! word
	dictbot: wort

For de->en, specify the direction with !deen

	you: !deen mist

And vice versa:

	you !ende mist

##To run locally
Change channel and nick in the code for testing purposes.

Make a virtualenv (using python 2.7!), e.g. with `virtualenvwrapper`, `mkvirtualenv dictbot`.

Get the required dependencies with `pip install -r requirements.txt`. Run with `python dictbot.py`.

##Dictionary
Dictionary service provided by [bab.la](http://en.bab.la/) who kindly are allowing this service to be run. Go check them out, it's pretty cool! It even has the translation for the word "crapulence".
