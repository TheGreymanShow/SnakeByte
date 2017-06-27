import cx_Freeze

executables = [cx_Freeze.Executable("snakebyte.py")]

cx_Freeze.setup(

	name = "SnakeByte",
	options = {"build_exe": {"packages": ["pygame"],"include_files":["apple1.png","apple2.png","background1.jpg","control_scr-2.jpg","gameover2.png","pausescr1.png","Snakehead2.png","startscreen4.jpg","abc.wav","apple1.wav","background1.wav","button1.wav","gameover3.wav","OpenSans-Bold.ttf"] }},
	description = "Snake Byte Game",
	executables = executables
	)
