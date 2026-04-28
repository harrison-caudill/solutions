PDFTEX  = docker run -ti \
	-e max_print_line=10000 \
	-v `pwd`:/root/work \
	-w /root/work \
	pdflatex \
	texfot \
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
	@$(MAKE) line --no-print-directory -e header="Pass 1: Generate the initial .aux file"
	@$(PDFTEX) $< >/dev/null 2>&1 && echo "Success" || $(PDFTEX) $<
	@$(MAKE) line --no-print-directory -e header="BIBTEX: Generate the bibliography entries from the .aux/.bib"
	$(BIBTEX) $(BUILD)/$(notdir $*)
	@$(MAKE) line --no-print-directory -e header="Pass 2: Build the Table of Contents"
	@$(PDFTEX) $< >/dev/null 2>&1 && echo "Success" || $(PDFTEX) $<
	@$(MAKE) line --no-print-directory -e header="Pass 3: Update page numbers from the ToC change"
	@$(PDFTEX) $< >/dev/null 2>&1 && echo "Success" || $(PDFTEX) $<
	@$(MAKE) line --no-print-directory -e header="Pass 4: Finalize page numbers after final labels update"
	@$(PDFTEX) $<

all: .dummy_builddir sak

line:
	@echo
	@echo
	@echo
	@echo
	@echo "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
	@echo "%% $(header)"
	@echo "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"

.dummy_builddir:
	mkdir -p $(BUILD)

clean:
	bash -c '. .shlib ; clean -pr'
	yes | rm -rf $(BUILD)

params:
	@$(MAKE) line --no-print-directory -e header="Building parameters file"
	echo "\def\\\\bookName{$(bookName)}" > $(BUILD)/bookParams.tex
	echo "\def\\\\chapterNum{$(chapterNum)}" >> $(BUILD)/bookParams.tex
	echo "\def\\\\problemNum{$(problemNum)}" >> $(BUILD)/bookParams.tex
	echo "\def\\\\buildPath{$(BUILD)}" >> $(BUILD)/bookParams.tex

sqrf: .dummy_builddir
	@$(MAKE) --no-print-directory -e bookName=sakurai params
	bin/figures.py -b sakurai -q
	bin/ref.py -b sakurai -q
	bin/qcad_export.py -b sakurai -q
	$(PDFTEX) \
	-jobname qrf \
	sakurai/qrf.tex \
	$(BUILD)/qrf.pdf

sak: .dummy_builddir
	@$(MAKE) --no-print-directory -e bookName=sakurai manual

manual: .dummy_builddir
	@$(MAKE) --no-print-directory -e bookName=$(bookName) params
	@$(MAKE) line --no-print-directory -e header="Building Python-Based Figures"
	bin/figures.py -b $(bookName)
	@$(MAKE) line --no-print-directory -e header="Exporting CAD Drawings"
	bin/qcad_export.py -b $(bookName)
	@$(MAKE) line --no-print-directory -e header="Consolidating References"
	bin/ref.py -b $(bookName)
	@$(MAKE) --no-print-directory $(bookName)/manual.pdf
	mv $(BUILD)/manual.pdf $(BUILD)/$(bookName).pdf

problem:
	@$(MAKE) --no-print-directory \
	-e bookName=sakurai \
	-e chapterNum=1 \
	-e problemNum=$(problemNum) \
	fullproblem

fullproblem: .dummy_builddir params
	@$(MAKE) line --no-print-directory -e header="Building Python-Based Figures"
	bin/figures.py -b $(bookName) -q
	bin/figures.py -b $(bookName) -c $(chapterNum) -p $(problemNum)
	@$(MAKE) line --no-print-directory -e header="Consolidating References"
	bin/ref.py -b $(bookName) -q
	bin/ref.py -b $(bookName) -c $(chapterNum) -p $(problemNum)
	@$(MAKE) line --no-print-directory -e header="Exporting CAD Drawings"
	bin/qcad_export.py -b $(bookName) -q
	bin/qcad_export.py -b $(bookName) -c $(chapterNum) -p $(problemNum)
	@$(MAKE) line --no-print-directory -e header="Building Problem"
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
