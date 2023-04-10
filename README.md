# Star Wars API task

#### _Modules required_
- requests
- matplotlib
- pyqt5

### Implementation
The script gets the command line arguments and calls the corresponding function.  
The possible commands are `search`, `cache` and `visual`.  
Cached requests are text files stored in a new directory.  


##### Search
Checks the cached requests, and executes a new request if the search has not been performed.
The new request is cached after completion.
It also searches for the world of the character, if the `--world` argument is passed.
If the string passed is something small, e.g. 'a', it will return all the characters that contain that string in their name.   
> Note: If the searched string is small, and the --world argument is passed, script will require a lot of time to complete. 
This can be improved with threading, but it was assumed that the user will search for a proper name.

Run with:  
```sh
python main.py search 'char_name'
python main.py search 'char_name' --world
```
##### Cache
Clears the cached requests.  
Run with:
```sh
python main.py cache
```



##### Visual
Creates an interactive window, that shows cached requests as points in a scatter plot.
On mouseover of a point it shows the results of that request and the time that it was cached.
On click of a point, it prints the result of that request on the console.
Run with:
```sh
python main.py visual
```

