## Inspiration
When I was younger, I would develop Discord bots and I would always have people come up to me and be like, "Can you make this bot for me?" and "Can you make this feature?" As a result of this nuisance that others have caused me, I have decided to make a Discord Bot Generator which creates a unique Discord bot for users. 

## What it does
Using MecSimCalc, the Bot Generator takes a user inputted Bot token, and sends the source code files over to a virtual private server and runs the Discord Bot using the user inputted token. This Discord Bot has all of the fundamental features necessary for running a server and even contains a function chatGPT moderation tool which deletes messages which are flagged as hateful, derogatory, or misinforming. 

## How I built it
I built this tool using MecSimCalc and a bunch of other Python libraries such as Discord.py, Paramiko, Asyncio, Json, Sqlite3, and many more! 

## Challenges I ran into
Overall development went pretty smoothly considering the time constraints however the majority of the issues I ran into were actually issues with MecSimCalc more than issues with my code. For example, after I had developed the tool such that it can run locally on my own computer, I had to port it to MecSimCalc and I ran into some issues with their filesystem being read-only for the files that were a part of the virtual environment. The method of fixing this was quite simple thankfully and I got it to work by just initializing a new JSON file each time I needed to have a config.json file. 

## Accomplishments that I'm proud of
Overall, I am quite proud of my project on MecSimCalc especially because I was able to make the entire thing myself without the help of anyone else. I am also quite proud of how I was able to make some features run much quicker than I expected considering that I was using Python as the main programming language. Another thing I'm quite proud of is how I was able to debug my code without the presence of any error codes in the terminal. The lack of error codes was due to the fact that the code was running on a VPS and I was unable to return the error codes which were outputted by the VPS after running the code. Despite this, I was able to overcome this and still have my project work. 

## What we learned
Throughout this hackathon, I learned more about how MecSimCalc works behind the scenes through my analysis of the error codes and prints of MecSimCalc. 

## What's next for Discord Bot Creator
This project has a lot of potential and I foresee that I will implement more features so that this project could potentially have some viable payment plans so as to monetize it. 
