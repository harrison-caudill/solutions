PDFTEX  = docker run -ti \
	-e max_print_line=10000 \
	-v `pwd`:/root/work \
	-w /root/work \
	pdflatex \
	pdflatex -halt-on-error \
	-output-directory $(BUILD)
DVITEX  = latex
DVIPS   = dvips
BIBTEX  = bibtex
PSPDF   = ps2pdf
DIA     = dia
CONVERT = convert
BUILD   = BUILD
cout    = combined
cname   = generic
book    =
dpi     = 300

%.eps: %.dia
	$(DIA) --export=$*.eps $<

%.jpg: %.xcf.bz2
	bzcat $< | $(CONVERT) -flatten - $*.jpg

%.jpg: %.eps
	$(CONVERT) $< $*.jpg

%.jpg: %.png
	$(CONVERT) $< $*.jpg

%.pdf: %.tex
	$(PDFTEX) $<
	$(PDFTEX) $<
	$(PDFTEX) $<

%.dvi: %.tex
	$(DVITEX) $<
	$(DVITEX) $<
	$(DVITEX) $<

%.ps: %.tex %.dvi
	$(DVIPS) -Ppdf $*.dvi

all: .dummy_builddir sak

.dummy_builddir:
	mkdir -p $(BUILD)

sak: .dummy_builddir
	make -e bookName=sakurai params
	bin/figures.py -b sakurai
	bin/qcad_export.py -s sakurai -d $(BUILD)
	echo "\def\\\\bookName{sakurai}" > $(BUILD)/bookParams.tex
	echo "\def\\\\buildPath{$(BUILD)}" >> $(BUILD)/bookParams.tex
	make sakurai/manual.pdf
	mv $(BUILD)/manual.pdf $(BUILD)/sakurai.pdf

clean:
	bash -c '. .shlib ; clean -pr'
	yes | rm -rf $(BUILD)

ref: .dummy_builddir
	bin/qcad_export.py -s ref -d $(BUILD)
	echo "\def\\\\bookName{ref}" > $(BUILD)/bookParams.tex
	echo "\def\\\\buildPath{$(BUILD)}" >> $(BUILD)/bookParams.tex
	make ref/ref.pdf

params:
	echo "\def\\\\bookName{$(bookName)}" > $(BUILD)/bookParams.tex
	echo "\def\\\\chapterNum{$(chapterNum)}" >> $(BUILD)/bookParams.tex
	echo "\def\\\\problemNum{$(problemNum)}" >> $(BUILD)/bookParams.tex
	echo "\def\\\\buildPath{$(BUILD)}" >> $(BUILD)/bookParams.tex

jackson: .dummy_builddir
	bin/qcad_export.py -s jackson -d $(BUILD)
	make -e bookName=jackson params
	make jackson/manual.pdf
	mv $(BUILD)/manual.pdf $(BUILD)/jackson.pdf

sqrf: .dummy_builddir
	make -e bookName=sakurai params
	bin/qcad_export.py -s sakurai/qrf -d $(BUILD)/sakurai
	$(PDFTEX) \
	-jobname qrf \
	sakurai/qrf.tex \
	$(BUILD)/qrf.pdf

problem: .dummy_builddir params
	bin/figures.py -b $(bookName) -c $(chapterNum) -p $(problemNum)
	bin/qcad_export.py -s sakurai/qrf -d $(BUILD)/sakurai
	bin/qcad_export.py -s $(bookName)/chapters/$(chapterNum)/problems/$(problemNum) -d $(BUILD)/$(bookName)/chapters/$(chapterNum)/problems
	$(PDFTEX) \
	-jobname $(bookName)-$(chapterNum)-$(problemNum)-raw \
	problem.tex \
	$(BUILD)/$(bookName)-$(chapterNum)-$(problemNum)-raw.pdf
	gs \
        -sDEVICE=pdfwrite \
        -dNOPAUSE \
        -dBATCH \
        -dFirstPage=2 \
        -sOutputFile=$(BUILD)/$(bookName)-$(chapterNum)-$(problemNum).pdf \
	$(BUILD)/$(bookName)-$(chapterNum)-$(problemNum)-raw.pdf
