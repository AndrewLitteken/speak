## Inspiration
The technology industry is growing faster than ever. Despite the need for more computer scientists, memorizing syntax can be daunting for beginners. This drew the inspiration for **speak: a compiler that understands** English instructions and translates them into compilable Python code. This makes coding more **accessible**, easy, and enjoyable.
## What it does
speak reads the text that the user inputs. It utilizes set of Python synonyms and keywords, **spaCy** dependencies trees and **Natural Language Processing**, as well as **NLTK** for determining the parts of speech for each instruction. 
## How we built it
We started by creating synonym data structures in **Python** to replace synonyms in the sentence and remove unneeded words. Then, we parse the sentence in Python and create syntax trees using nested logic, checking aspects such as word parts of speech to determine the dependencies. Lastly, we incorporated this code into a **centOS server** web app on that makes calls to it using **JavaScript** and downloads the translated Python code using download.js.
## Challenges we ran into
Because this compiler was a completely new and novel idea, there were no precedents to use as inspiration. We ran into many difficult concepts, problems, and implementation decisions. These decisions ranged from pivoting away from our initial NLP backend flow on NodeRED to adapting NLTK to determine overall meaning rather than the sentiment of user input.
## Accomplishments that we're proud of
We are incredibly proud to have created a completely **novel** product in the space of **one weekend at TreeHacks**. We solved problems, collaborated, struggled, and found eventual success. Notably, we are quite proud of the fact that we **figured out** how to implement this tool without having to use expensive online Natural Language Classifiers. 
## What we learned
**spaCy + NLTK + Natural Language Processing** concepts + how to create **syntax trees** + how to process the meaning of English text + how to configure a centOS Apache web server to run Python + how to use a **domain.com domain**
## What's next for speak
We want to continue with speak and are excited to **expand upon it in the future**. We also hope to iterate upon it until it is ready for a software patent or copyright. 
