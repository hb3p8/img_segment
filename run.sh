python main.py -s 1 -a 10 1.png -o first
python main.py -s 1 -a 10 2.png -o second
python main.py -s 1 -a 10 3.png -o third

python main.py -s 1 -a 4 1.png -o appTestSmall1
python main.py -s 1 -a 10 1.png -o appTestMid1
python main.py -s 1 -a 16 1.png -o appTestLarge1

python main.py -s 2 -a 4 2.png -o appTestSmall2
python main.py -s 2 -a 10 2.png -o appTestMid2
python main.py -s 2 -a 16 2.png -o appTestLarge2

python main.py -s 2 -a 4 3.png -o appTestSmall3
python main.py -s 2 -a 10 3.png -o appTestMid3
python main.py -s 2 -a 16 3.png -o appTestLarge3

python main.py -s 1 -a 10 1.png -o stepTestSmall1
python main.py -s 8 -a 10 1.png -o stepTestMid1
python main.py -s 15 -a 10 1.png -o stepTestLarge1

python main.py -s 1 -a 10 2.png -o stepTestSmall2
python main.py -s 8 -a 10 2.png -o stepTestMid2
python main.py -s 15 -a 10 2.png -o stepTestLarge2

python main.py -s 1 -a 10 3.png -o stepTestSmall3
python main.py -s 8 -a 10 3.png -o stepTestMid3
python main.py -s 15 -a 10 3.png -o stepTestLarge3

python main.py -s 1 -a 4 1.png -m cross -o medianCross1
python main.py -s 1 -a 4 1.png -m plus -o medianPlus1
python main.py -s 1 -a 4 1.png -m square -o medianSquare1

python main.py -s 1 -a 4 2.png -m cross -o medianCross2
python main.py -s 1 -a 4 2.png -m plus -o medianPlus2
python main.py -s 1 -a 4 2.png -m square -o medianSquare2

python main.py -s 1 -a 4 3.png -m cross -o medianCross3
python main.py -s 1 -a 4 3.png -m plus -o medianPlus3
python main.py -s 1 -a 4 3.png -m square -o medianSquare3

#pdflatex -output-directory=./build/ lab1.tex
#python main.py -gr -s 4 -a 10 1.png --maxw 65 --letters 8
#python main.py -gr -s 4 -a 10 2.png --maxw 35 --letters 6
#python main.py -gr -s 2 -a 8 3.png --maxw 35 --minw 10 --letters 5
# python main.py -gr -s 2 -a 10 4.png --maxw 35 --minw 10 --letters 7


#python main.py -gl -s 2 -a 12 3.png --maxw 35 --minw 7
# python main.py -gl -s 2 -a 10 new.png --maxw 35 --minw 10
