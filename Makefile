PDFTEX  = docker run -ti \
	-e max_print_line=10000 \
	-v `pwd`:/root/work \
	-w /root/work \
	pdflatex \
	pdflatex -halt-on-error \
	-output-directory $(BUILD)
BIBTEX  = docker run -ti \
	-v `pwd`:/root/work \
	-w /root/work \
	pdflatex \
	bibtex
PSPDF   = ps2pdf
CONVERT = convert
BUILD   = BUILD

%.pdf: %.tex
	$(PDFTEX) $<
	$(BIBTEX) $(BUILD)/manual
	$(PDFTEX) $<
	$(PDFTEX) $<

all: .dummy_builddir sak

.dummy_builddir:
	mkdir -p $(BUILD)

clean:
	bash -c '. .shlib ; clean -pr'
	yes | rm -rf $(BUILD)

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
	bin/figures.py -b sakurai -q
	bin/ref.py -b sakurai -q
	bin/qcad_export.py -b sakurai -q
	$(PDFTEX) \
	-jobname qrf \
	sakurai/qrf.tex \
	$(BUILD)/qrf.pdf

sak: .dummy_builddir
	make -e bookName=sakurai params
	bin/figures.py -b sakurai -q
	bin/figures.py -b sakurai
	bin/ref.py -b sakurai -q
	bin/ref.py -b sakurai
	bin/qcad_export.py -b sakurai -q
	bin/qcad_export.py -b sakurai
	echo "\def\\\\bookName{sakurai}" > $(BUILD)/bookParams.tex
	echo "\def\\\\buildPath{$(BUILD)}" >> $(BUILD)/bookParams.tex
	make sakurai/manual.pdf
	mv $(BUILD)/manual.pdf $(BUILD)/sakurai.pdf

problem: .dummy_builddir params
	bin/figures.py -b $(bookName) -q
	bin/figures.py -b $(bookName) -c $(chapterNum) -p $(problemNum)
	bin/ref.py -b $(bookName) -q
	bin/ref.py -b $(bookName) -c $(chapterNum) -p $(problemNum)
	bin/qcad_export.py -b sakurai -q
	bin/qcad_export.py -b sakurai -c $(chapterNum) -p $(problemNum)
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
