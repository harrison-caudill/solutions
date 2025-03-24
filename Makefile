PDFTEX  = docker run -ti \
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

all: .dummy_builddir jackson

.dummy_builddir:
	mkdir -p $(BUILD)

clean:
	bash -c '. .shlib ; clean -pr'
	yes | rm -rf $(BUILD)

images:
	for f in $(find . -type f -name *.dxf | grep -v _trimmed.png$) ; do n=$(BUILD)/`echo $f | sed -e 's/.dxf$/.png/'` ; echo make $n ; done

jackson: .dummy_builddir
	bin/qcad_export.py -s jackson -d $(BUILD)
	echo "\def\\\\bookName{jackson}" > $(BUILD)/bookParams.tex
	echo "\def\\\\buildPath{$(BUILD)}" >> $(BUILD)/bookParams.tex
	make jackson/manual.pdf
	mv $(BUILD)/manual.pdf $(BUILD)/jackson.pdf
