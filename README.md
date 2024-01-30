# SGL - Simple Graphics Language

## Intro
This is my programming language called SGL. It's a personal project I'm doing to learn compiler design, simple graphics and just for fun. The compiler is built in python and is heavily inspired by the [Teeny Tiny Compiler](https://github.com/AZHenley/teenytinycompiler) by [Austin Z. Henley](https://austinhenley.com/blog.html). It's really a transpiler to html and js to serve a canvas element for drawing graphics.

## Features
### Sections
#### #CONFIG#
The #CONFIG# Section is necessary for setting up every program, this is the "boilerplate" of SGL

In this section you set up the following variables for the canvas:

```
SCREEN_HEIGHT
SCREEN_WIDTH
SCREEN_BG
SCREEN_CLEAR_DELAY
SCREEN_GRIDSIZE
```

Usage example:

This code generates an html canvas with width and height 200*8 px, black background and a delay of 0.5 seconds on every clear call.
```
#CONFIG#
SCREEN_HEIGHT = 200
SCREEN_WIDTH = 200
SCREEN_BG = [0 0 0]
SCREEN_CLEAR_DELAY = 0.5
SCREEN_GRIDSIZE = 8
```

You can also use these variables later on in the code.

Standard values are:
```
SCREEN_HEIGHT = 100
SCREEN_WIDTH = 100
SCREEN_BG = [0 0 0]
SCREEN_CLEAR_DELAY = 0
SCREEN_GRIDSIZE = 5
```

#### #FUNCTIONS#
Here you can create functions to use in the main section

Usage example:

This SGL code
```
#FUNCTIONS#

appr(v) = {
    (4*v*(180-v))/(40500-v*(180-v))
}

sin(X) = {
    x = X
    loop {
        if x >= 0 {
            break
        }
        x = 6.28 + x
    }
    x = x%6.28
    x = x*360/6.28
    if x >= 180{
        -appr(x-180)
    }
    (appr(x))
}
```
Generates this javascript
```
function appr(v){
    return (4*v*(180-v))/(40500-v*(180-v))
}

function sin(X){
    let x=X
    while(true){
        if(x>=0){
            break
        }
        x=6.28+x
    }
    x=x%6.28
    x=x*360/6.28
    if(x>=180){
        return (-appr(x-180))
    }
    return (appr(x))
}
```

#### #MAIN#
This is the main part of your program ekvivalent to 
'int main{}' in c/c++

### Math

The available operators in SGL are:
* addition (+)
* subtraction (-)
* multiplikation (*)
* division (/)
* modulo (%)
* exponentiation

You can also use parenthesis for altering the order of operations

### Statements

#### if
Your usual if statement

Usage:
```
if x + 3 == y {
    print(x)
}
```

#### loop
A continous loop until break is called

Usage:
```
i = 0
loop {
    i = i + 1
    print(i)
    if i == 10 {
        break
    }
}
```

#### break
Use this to break the loop statement

#### draw
Draw to the screen.
Three parameters (x y color)

Usage:
```
draw(10 10 [255 255 255])
```
This fills the grid at position x = 10, y = 10 with the color white

#### clear
This waits 'SCREEN_CLEAR_DELAY' seconds and then clears the screen by filling it with the color 'SCREEN_BG'

Usage:
```
clear()

i = 0
loop {
    draw(i i [0 255 0])
    clear()
    i = i + 1
    if i == 50 {
        break
    }
}
```
This example animates a pixel going from (0 0) to (50 50) in a straight line.

#### print
This prints (console.log) the given value to the console.

Usage:
```
print(5)
print(10.5)
print(10/5)
print(val)
print(x+y)
```

#### random
Gives a random number between 0 and 1

Usage:
```
print(random())
x = random()
x = random()*5
```

#### floor
Floors the given number to a whole number.

Usage:
```
print(floor(3.5))
print(floor((x+1)/3))
print(floor(x/y))
```

## What's Coming
* A Online compiler
* Actually useful lists
* A sleep method (delay without clear)
* Module functionality
* Standard library

## Quick start

This is a short guide on how to draw a square scaling up and down in SGL

First of, create a new file called 'square.sgl' in the same folder as the compiler.

Then in square.sgl write this config section:
```
#CONFIG#
SCREEN_WIDTH = 200
SCREEN_HEIGHT = 200
SCREEN_BG = [0 0 0]
SCREEN_CLEAR_DELAY = 0.1
SCREEN_GRIDSIZE = 1
```

This will create a 200 by 200 canvas with a black background and set the clear-delay to 0.1 seconds.

To test this and to test the later steps you can open a terminal in the current folder and run:
```
python compiler.py square.sgl
```
And then open the generated square.sgl.html in your browser

Then create a function for drawing a square.
To do this we will start by drawing the upper line like this:
```
#FUNCTIONS#
drawSquare(x0 y0 w h) = {
    x = x0
    y = y0
    x1 = x0+w
    y1 = y0+h
    loop {
        if x >= x1 {
            break
        }
        draw(x y [255 255 255])
        x += 0.5
    }
}
```
This works because we, starting from the upper left corner (x0 y0), draw the point (x y) white and increment x until we reach the upper right coner (x0+w y0).

We'll do a similar appraoch for the remaining sides like this:
```
#FUNCTIONS#
drawSquare(x0 y0 w h) = {
    x = x0
    y = y0
    x1 = x0+w
    y1 = y0+h
    loop {
        if x >= x1 {
            break
        }
        draw(x y [255 255 255])
        x = x+ 0.5
    }
    loop {
        if y >= y1 {
            break
        }
        draw(x y [255 255 255])
        y = y+ 0.5
    }
    loop {
        if x <= x0 {
            break
        }
        draw(x y [255 255 255])
        x = x- 0.5
    }
    loop {
        if y <= y0 {
            break
        }
        draw(x y [255 255 255])
        y = y-0.5
    }
}
```

And that's the function all done :)

Now we'll start the main section by drawing a square using the function.

```
#MAIN#

drawSquare(10 10 SCREEN_WIDTH -20 SCREEN_HEIGHT-20)
```

Viola! You have now made a square on a canvas.

Now we will start animating it shrinking and growing.
```
scale = 1
loop {
    if scale >= 0.5 {
        break
    }
    clear()
    width = (SCREEN_WIDTH - 20)*scale
    height = (SCREEN_HEIGHT - 20)*scale
    drawSquare(SCREEN_WIDTH/2-width/2 SCREEN_HEIGHT/2-height/2 width height)
    scale = scale - 0.025
}
```

This will shrink the square from large to small. Then all we need to do is to scale it back in the same way and then loop that over and over again, forever. This will be our final main section

```
#MAIN#
scale = 1
loop{
loop {
    if scale <= 0.5 {
        break
    }
    clear()
    width = (SCREEN_WIDTH - 20)*scale
    height = (SCREEN_HEIGHT - 20)*scale
    drawSquare(SCREEN_WIDTH/2-width/2 SCREEN_HEIGHT/2-height/2 width height)
    scale = scale - 0.025
}
loop {
    if scale >= 1 {
        break
    }
    clear()
    width = (SCREEN_WIDTH - 20)*scale
    height = (SCREEN_HEIGHT - 20)*scale
    drawSquare(SCREEN_WIDTH/2-width/2 SCREEN_HEIGHT/2-height/2 width height)
    scale = scale + 0.025
}
}
```

And thats it, we are done!

You have now learned how to use the Config, Functions and main sections together to create your graphics.

Feel free to experiment with this. Maybe you can make the square edges squigly or do something cool by varying the colours. 

I hope you are going to have just as fun using SGL as I've been having creating it.

