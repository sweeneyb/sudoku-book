## prereq
Install the texlive group:
```
pacman -Syu texlive
```

## PDF output
```
texi2pdf --pdf first.tex
```

## html output
```
make4ht -u first.tex
```