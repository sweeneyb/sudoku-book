## prereq
Install the texlive group:
```
pacman -Syu texlive
```

## PDF output
```
texi2pdf --pdf first.tex
```
or
```
pdflatex sudoku.tex
```

## html output
```
make4ht -u first.tex
```