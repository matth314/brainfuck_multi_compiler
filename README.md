# brainfuck_multi_compiler

 * Compile Brainfuck, FuckFuck, DNA# and Ook! into Python, C, Brainfuck, FuckFuck, DNA# or Ook! whenever it is possible
 * Run Brainfuck, FuckFuck, DNA# and Ook! programs efficiently
 * Can be used as a Python library
 * Contain a small library of programs in different languages
 
## Usage:
Default input and output are stdin and stdout.
  * `./brainfuck.py -h` print help and usage
  * `./brainfuck.py -r -i progs/brainfuck/hello_world.bf` run
  * `./brainfuck.py -c -i progs/brainfuck/hello_world.bf -ol FuckFuck` compile the input program into FuckFuck 
  * `./brainfuck.py -c -i progs/brainfuck/hello_world.bf -ol DNA#-helix -i dna` compile the input program into DNA and store it to the `dna` file. 
  * `./brainfuck.py -c -ol C -i progs/brainfuck/hello_world.bf | gcc -o hello_world -xc -w - && ./hello_world.exe` Compile the brainfuck program into C, compile it with gcc, and run it.
  *   `./brainfuck.py -c -ol DNA#-helix -i progs/brainfuck/hello_world.bf | ./brainfuck.py -r -il DNA#` Compile the brainfuck program into DNA#, and then read the input for a DNA# program and run it.

## Language supported
* Brainfuck
https://fr.wikipedia.org/wiki/Brainfuck
* FuckFuck
https://esolangs.org/wiki/Fuckfuck
http://web.archive.org/web/20050318095341/http://www.chilliwilli.co.uk/ff/
* Ook
 https://esolangs.org/wiki/Ook!
* DNA#
https://esolangs.org/wiki/DNA-Sharp
