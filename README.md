# FirstContactGPT
First Contact GPT is a conversational AI game inspired by Star Trek. In this game, you take on the role of Joseph Rybar, the captain of the USS Carpathia, who is sent out to establish contact with an advanced, unknown alien race. Your objective is to communicate with the alien race and negotiate a personal meeting with their representatives.

* Add Game image
 
The game is developed in Python and uses OpenAI's GPT API model to simulate conversations with the alien race. I created this game as a tech demo to showcase how recent advances in AI could revolutionize the future of gaming. The game features a system I call the "AI Mission Monitor in the Loop."

* Add image

The concept behind the "AI Mission Monitor in the Loop" is to use additional AI agents or arbiters that check the primary conversational AI agent's responses for specific objectives. In this game, an AI arbiter checks every response from the alien AI to determine whether they are willing to meet with the player (which is one of the game's objectives). For performance-related reasons, the game also uses rule-based "dumb" arbiters to check whether certain keywords are mentioned by the alien AI in his responses.

## Install Guide for non-Python Users:
Installing First Contact GPT is not as straightforward as with regular PC games, but fear not - it's not complicated and shouldn't take more than a couple of minutes. Here is what you will need:
1. Python with two additional libraries
2. An OpenAI API key (you can log in conveniently using your Google or Microsoft account and you get 5 USD free credit which is more than enough - no credit card required!)

### How to install the requirements:
1. Download and install the latest version of Python from [python.org](https://www.python.org/)
2. **When installing Python it is important to tick the *"Add Python 3.X to PATH"* option!**
3. Once Python is installed, open the Command Prompt. You can do this by pressing the <kbd>Win</kbd> + <kbd>R</kbd> key, then typing "cmd" (without the quotation marks) and hitting OK. This will launch the Command Prompt window. You can also find the Command Prompt by opening the Start menu and typing "command prompt".
4. Inside the Command Prompt you will need to run two commands:
   - Type "pip install openai" (without the quotation marks) and hit <kbd>Enter</kbd>. This will install the OpenAI Python package.
   - Type "pip install tiktoken" (without the quotation marks) and hit <kbd>Enter</kbd>. This will install the Python package to count the number of words/tokens in your prompts. Don't worry, this has nothing to do with TikTok.
5. You can close the Command Prompt window
6. Download and unzip First Contact GPT to any folder on your PC. You can download the latest version of the game [here](https://www.python.org/).
7. Create an OpenAI developer account [here](https://platform.openai.com). You can conveniently use your Google or Microsoft account.
8. Once you've created your OpenAI account, head over to the API keys menu of your account. You can find it by clicking on your account in the upper right corner.
9. Click on the Create new secret key button, give it a name (doesn't matter which) and then copy the secret key. You will need to paste it into the game's source code in the next step.
10. Open *FirstContactGPT.py* in the folder where you unzipped the game in a text editor. Default Notepad will do just fine. You can drag and drop the file into Notepad. The 10th line of code reads:
```python
openai.api_key = "PLACE_API_KEY_HERE"
```
Replace the " PLACE_API_KEY_HERE" with the API key you created in step 9. You should still have it copied in your clipboard. The line of code should like like this:
```python
openai.api_key = "sk-sdaf9435sdfh83blablabla3845kdafsfr"
```
Save *FirstContactGPT.py* and close the text editor. **Now you can run the game by double-clicking on *FirstContactGPT.py*.**

## Next steps - Tinkering With the Source Code

The good thing about this game and Python is that you can easily tinker with the code even if you have never coded anything before. Here are some examples of how you can change the First Contact GPT:

### Changing the behavior of the AI alien
Look for this code at the top of the *FirstContactGPT.py* file and change it however you wish.
```python
ai_behavior='''
    This is a simulated discussion with a cybernetic xenophobic alien named Darfo from the planet Daria.
    Your race is called the Darian Collective. Your alien race is made up of self-replicating artificial intelligent aliens.
    You speak in scientific metaphors and give short and rude answers.
    '''
```
It's up to you how you change it.

### Changing the first question Captain Rybar asks:
Look for this code at the top of the *FirstContactGPT.py* file and change it however you wish.
```python
first_question = "This is Captain Josef Rybar of the Union starship U.S.S Carpathia. We come in peace and with the utmost respect for your culture and way of life. We are eager to establish peaceful communication and to learn from one another. We hope that our encounter will lead to mutual understanding and a lasting relationship. Please respond if you are able, and let us know how we may respectfully proceed.\n"
    '''
```
You will find it right below the AI alien's behavior description.

### Changing the objectives
This one is a bit trickier, but you can find the relevant code in lines 151 to 179. Try changing it and if it works that perfect.

## Credits
Craphics created with [Leonardo.ai](https://leonardo.ai/) and edited in [paint.net](https://www.getpaint.net/).
