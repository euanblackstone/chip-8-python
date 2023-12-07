all:
	cp main.py chip8
	chmod +x chip8

clean:
	rm chip8
	rm -rf __pycache__
	