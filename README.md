# PygameLife
Conway's "Game of Life", created with Python3 and Pygame.

This started with an example program for one of my University papers. It was quite a bad example
to start with and did such things as redraw the *entire* grid each update.

I've chopped out as many 'for' loops as possible, and created a pygame surface which the grid gets drawn to once.
This BG surface then gets blitted to the screen surface on every update instead of using the for loop it used to
have. The end effect was highly noticable especially at the higher resolutions (Imagine iterating through a 1920x1080 loop. Total time soak).

Further improvements are switching to a class based structure (still evolving), and splitting program parts to
individual files for easier management. Plus the beginnings of a menu.

End goal is to make this a decent "game" of sorts, with options for resolution, colours, saving the start grid.

GPLv3.0 Licence. Anybody is welcome to hack on it.
