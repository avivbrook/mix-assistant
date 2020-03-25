# mix-assistant

The program takes a list of songs you want in your DJ set and suggests to you which songs to transition into based on the key and BPM of the current song. You give the program Beatport links to all the songs you want in your set because Beatport has accurate key and BPM info that the program can read.

1. Example of the first run-through (where the program has to scrape the Beatport links):
![alt text](https://raw.githubusercontent.com/avivbrook/mix-assistant/master/images/scrape.png "Web Scraping")
This process could take a minute depending on your internet connection.

2. Example of selecting a song and getting suggestions for the next one:
![alt text](https://raw.githubusercontent.com/avivbrook/mix-assistant/master/images/suggestions.png "Suggestions")
G min and A min sound good with D min hence the suggestions. Also, you'll notice it shows a song with 124 BPM first then songs with 126 BPM which is close to 124. The more songs you have in your database the better the suggestions (`links2` has ~50 songs, try that one out too).

## Prerequisites

This is written in Python 3. I know most Mac computers come preinstalled with Python 2 which might work though I haven't tested it. If you run into any issues, just make sure you have Python 3 installed.

## Usage

Run the program from your terminal by: `python3 Mix.py`.

`links` is the file that will contain the songs you want in your set. It has to be in the same directory as `Mix.py`. I've provided a sample `links` file that contains some songs that I like. The links you provide have to be Beatport (since it has BPM and key) and they have to follow the same format. The program will tell you if it can't read any of the links you've provided.

Each time you update the `links` file and you re-run the program, it will scan the links you've provided (which takes a bit of time). It stores all the info in a hidden file called `.db` in the same directory. If you run the program again without updating `links`, it will get the data very quickly since it's going to read it from `.db` without having to scan Beatport. Keep that in mind to save time when using this.

## Feedback

I've only spent about a day on this so far so it's not the prettiest as this isn't my highest priority project at the moment. Feel free to shoot me an email at avivbrook@gmail.com if you have any questions or comments.

### To-Do

* Add an option to go back if you regret choosing some song.
* Add options to input music from local files or something other than Beatport.
* Make the interface prettier (preferably without having to make a GUI). Any suggestions are accepted.

## Author

* **Aviv Brook** - [avivbrook](https://github.com/avivbrook)
