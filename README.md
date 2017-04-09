# NITWBot

Hi, this bot is pretty awful but there's salvagable components.

You'll need to add your own Discord Bot Token to the config/token file.

You'll also need to work out all the dependencies. There might also be missing files/folders for logging/image generation.

Finally you'll need to sort out clearing out the image log: I just used a cronjob to clear any files in the folder that were older than 5 minutes.


Things you'll want to Fix first:

The way different characters is managed is awful: there's like 4 different parts of the code that manage this. Your first priority should be moving all the character stuff to a config file specific to characters.
This will include the word, colour of text and speech bubble position. You will also want to add easter eggs to this.

Speaking of, easter eggs are currently a reallyt sloppy quickbit of code. Again, move this into a config file.

Setting up the server whitelist is ASS as you need to edit the JSON manually. Create a way to do this programatically.

Add support for Emoji conjoining and custom emojis.



REALLY YOU SHOULD SCRAP ALL THE BOT STUFF AND JUST USE THE IMAGE GENERATION IN /nitw-text-stitch. IT WILL BE FAR EASIER TO WORK WITH.

Okay good luck.
