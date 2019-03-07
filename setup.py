import cx_Freeze

executables = [cx_Freeze.Executable("pgPc.py")]

cx_Freeze.setup(name="Megaman VII Endless Runner",
                options={"build_exe": {"packages": ["pygame"],
                                       "include_files": ['rp1.png', 'rp2.png', 'rp3.png', 'rp4.png', 'rp5.png',
                                                         'rp6.png',
                                                         'rp7.png', 'rp8.png', 'rp9.png',
                                                         'rp10.png', 'jp1.png', 'jp2.png', 'jp3.png', 'jp4.png',
                                                         'jp5.png',
                                                         'jp6.png', 'jp7.png', 'jp8.png', 'jp9.png',
                                                         'jp10.png', 'b1.png', 'b2.png', 'b3.png', 'b4.png', 'b5.png',
                                                         'b6.png',
                                                         'b7.png', 'b8.png', 'b9.png', 'm1-1.png', 'm1-2.png',
                                                         'm1-3.png', 'm1-4.png',
                                                         'm1-5.png', 'm2-1.png', 'm2-2.png', 'm2-3.png', 'm2-4.png',
                                                         'db1.png', 'db2.png', 'db3.png',
                                                         'e1.png', 'e2.png', 'e3.png', 'e4.png', 'e5.png', 'e6.png',
                                                         'e7.png', 'e8.png', 'e9.png', 'e10.png',
                                                         'e11.png', 'e12.png', 'e13.png', 'e14.png', 'e15.png',
                                                         'e16.png', 'e17.png', 'fire1.png', 'fire2.png',
                                                         'fire3.png', 'fire4.png', 'missile.png', 'warning.png',
                                                         'spikes1.png', 'introimg.png', "bg.png", "s1bg.png", 'go.png',
                                                         'IWBTB OST MEGAMAN.wav', 'Mega_Man_7_OST_Stage_Select.wav',
                                                         'js.wav', 'deathsound.wav', 'explosion.wav',
                                                         'shoot.wav', 'm2shoot.wav', 'missilelunch.wav', 'alert.wav']}},
                executables=executables
                )
