
        $H
        G21
         M3
(Header end.)
G21 (All units in mm)

(Start cutting path id: path1300)
(Change tool to Cylindrical cutter)

G00 Z0.000000
G00 X5.000000 Y5.114601

G00 Z0 (Fast pre-penetrate)
G01 Z-1.224000 F100.0(Penetrate)
G01 X5.000000 Y70.114599 Z-1.7000 F150.000000
G01 X20.000000 Y70.114599 Z-1.7000
G01 X20.000000 Y5.114601 Z-1.7000
G01 X15.000000 Y5.114601 Z-1.7000
G01 X15.000000 Y65.114599 Z-1.7000
G01 X10.000000 Y65.114599 Z-1.7000
G01 X10.000000 Y5.114601 Z-1.7000
G00 Z0.000000

(End cutting path id: path1300)


(Start cutting path id: path1300)
(Change tool to Cylindrical cutter)

G00 Z0.000000
G00 X5.000000 Y5.114601

G00 Z0 (Fast pre-penetrate)
G01 Z-1.224000 F100.0(Penetrate)
G01 X5.000000 Y70.114599 Z-0.7000 F150.000000
G01 X20.000000 Y70.114599 Z-0.7000
G01 X20.000000 Y5.114601 Z-0.7000
G01 X15.000000 Y5.114601 Z-0.7000
G01 X15.000000 Y65.114599 Z-0.7000
G01 X10.000000 Y65.114599 Z-0.7000
G01 X10.000000 Y5.114601 Z-0.7000
G00 Z0.000000

(End cutting path id: path1300)


(Footer)
M5
G00 X0.0000 Y0.0000
M2
       
        G00 Z5
        G10 P0 L20 Z0
        
        G00 Z00.000000
        $H
        