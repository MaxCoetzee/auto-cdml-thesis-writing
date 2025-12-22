# Exposé

FILE := expose
OUT  := build
# expand args at runtime, since `jobname` doesn't exist outside targets 
TEX_FLAGS = -interaction=nonstopmode -outdir="$(OUT)" -pdf -halt-on-error -jobname="$(jobname)" $(FILE)

.PHONY: pdf
pdf:
	+latexmk $(TEX_FLAGS)

.PHONY: watch
watch:
	+latexmk $(TEX_FLAGS) -pvc 

.PHONY: clean
clean:
	rm $(filter-out $(OUT)/.gitignore, $(wildcard $(OUT)/*))