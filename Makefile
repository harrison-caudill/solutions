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
	make -e bookName=sakurai manual

manual: .dummy_builddir
	make -e bookName=$(bookName) params
	bin/figures.py -b $(bookName) -q
	bin/figures.py -b $(bookName)
	bin/ref.py -b $(bookName) -q
	bin/ref.py -b $(bookName)
	bin/qcad_export.py -b $(bookName) -q
	bin/qcad_export.py -b $(bookName)
	echo "\def\\\\bookName{$(bookName)}" > $(BUILD)/bookParams.tex
	echo "\def\\\\buildPath{$(BUILD)}" >> $(BUILD)/bookParams.tex
	make $(bookName)/manual.pdf
	mv $(BUILD)/manual.pdf $(BUILD)/$(bookName).pdf

problem: .dummy_builddir params
	bin/figures.py -b $(bookName) -q
	bin/figures.py -b $(bookName) -c $(chapterNum) -p $(problemNum)
	bin/ref.py -b $(bookName) -q
	bin/ref.py -b $(bookName) -c $(chapterNum) -p $(problemNum)
	bin/qcad_export.py -b $(bookName) -q
	bin/qcad_export.py -b $(bookName) -c $(chapterNum) -p $(problemNum)
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
