

all:
	pdflatex -halt-on-error  main
	#pdflatex -halt-on-error  -draftmode -interaction=nonstopmode main
	bibtex  main # or biber
	pdflatex -halt-on-error  -draftmode -interaction=nonstopmode main
	pdflatex -halt-on-error  -interaction=nonstopmode main

clean:
	rm -f *.aux *.log main.pdf *.out *.bbl *.blg
