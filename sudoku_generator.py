# !/usr/bin/python
import sys
from Sudoku.Generator import *
import base64
import qrcode


from reportlab.pdfgen import canvas

def get_ident_str(board):
    rep = board.get_raw_numbers()
    encoding = base64.b64encode( bytes (rep, 'utf-8'))
    return encoding.decode('utf-8')

# setting difficulties and their cutoffs for each solve method
difficulties = {
    'easy': (35, 0), 
    'medium': (81, 5), 
    'hard': (81, 10), 
    'extreme': (81, 15)
}

# getting desired difficulty from command line
difficulty = difficulties[sys.argv[2]]

# constructing generator object from puzzle file (space delimited columns, line delimited rows)
gen = Generator(sys.argv[1])

# applying 100 random transformations to puzzle
gen.randomize(100)

# getting a copy before slots are removed
initial = gen.board.copy()

# applying logical reduction with corresponding difficulty cutoff
gen.reduce_via_logical(difficulty[0])

# catching zero case
if difficulty[1] != 0:
    # applying random reduction with corresponding difficulty cutoff
    gen.reduce_via_random(difficulty[1])


# getting copy after reductions are completed
final = gen.board.copy()

# printing out complete board (solution)
print("The initial board before removals was: \r\n\r\n{0}".format(initial))

# printing out board after reduction
print("The generated board after removals was: \r\n\r\n{0}".format(final))

initial_string = get_ident_str(initial)+"-0"
print("Raw Data: \r\n\r\n{0}".format(initial_string))

img = qrcode.make("https://briansweeney.dev/sudoku/"+initial_string)
img.save("qrcode.png")

# make a 6x9  page https://docs.reportlab.com/reportlab/userguide/ch2_graphics/
my_canvas = canvas.Canvas("hello.pdf", pagesize=(432, 648))
my_canvas.setFont("Courier", 18)
for index, row in final.rows.items():
    foo = ""
    for x in row:
        if x.value is 0:
            foo = foo + "  "
        else:
            foo = foo + str(x.value) + " "
        if (x.col +1) % 3 == 0:
            # foo = foo +"|"
            foo = foo + " "
        else:
            foo = foo + " "
    my_canvas.drawString(75, 600 - (20*2*index), f"{foo}")
    # if (index+1) % 3 == 0 and index is not 8:
        # my_canvas.drawString(75, 600 - (20*(2*index)), f"_  _  _  _  _  _  _  _  _  ")
    # output.append(map(str, [x.value for x in row]))
# my_canvas.drawString(100, 750, f"{final}")
my_canvas.setFont("Helvetica", 12)
my_canvas.drawString(100, 175, f"Hint #1")
my_canvas.drawString(225, 175, f"Hint #2")
my_canvas.drawImage("qrcode.png", 75,75, width=100,height=100,mask=None)
my_canvas.drawImage("qrcode.png", 200,75, width=100,height=100,mask=None)

line_y = 510
my_canvas.line(50,line_y,350,line_y)
line_y = 380
my_canvas.line(50,line_y,350,line_y)

line_x = 165
my_canvas.line(line_x,260,line_x,615)

line_x = 260
my_canvas.line(line_x,260,line_x,615)

my_canvas.save()