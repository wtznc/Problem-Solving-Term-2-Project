# Problem Solving for Computer Science - Assignment
### Term 2 Project
Wojciech Tyziniec  
Computer Science (Year 1)  
Goldsmiths, University of London


## Test Data





|Status|Objects|Initial states|Goal states|
|---|---|---|---|
|:heavy_check_mark:|<sup>table1 table2 A</sup>|<sup>ON(A,table1) HEAVIER(table1,A) HEAVIER(table2,A) CLEAR(A) CLEAR(table2)</sup>|<sup>CLEAR(table1) CLEAR(A)</sup>|
|:heavy_check_mark:|<sup>table1 table2 A table3 table4 B</sup>|<sup>ON(A,table1) HEAVIER(table1,A) HEAVIER(table2,A) HEAVIER(table3,A) CLEAR(A) CLEAR(table2) ON(B,table3) HEAVIER(table3,B) HEAVIER(table4,B) CLEAR(B) CLEAR(table4) HEAVIER(table4,A) HEAVIER(table1,B)</sup>|<sup>ON(A,table3) ON(B,table4)</sup>|
|:heavy_check_mark:|<sup>table1 table2 table3 A B</sup>|<sup>ON(A,table1) ON(B,table2) CLEAR(table3) HEAVIER(table1,A) HEAVIER(table2,B) HEAVIER(table2,A) HEAVIER(table3,A) HEAVIER(table3,B) CLEAR(A) CLEAR(B)</sup>|<sup>ON(A,table2)</sup>|
|:heavy_check_mark:|<sup>A B C D E table1 table2 table3 table4 table5 table6 table7 table8 table9 table10</sup>|<sup>ON(A,table1) ON(B,table2) ON(C,table3) ON(D,table4) ON(E,table5) CLEAR(A) CLEAR(B) CLEAR(C) CLEAR(D) CLEAR(D) CLEAR(E) HEAVIER(A,table1) HEAVIER(B,table2) HEAVIER(C,table3) HEAVIER(D,table4) HEAVIER(E,table5) CLEAR(table6) CLEAR(table7) HEAVIER(table6,A) HEAVIER(table7,B) CLEAR(table8) CLEAR(table9) CLEAR(table10) HEAVIER(table8,C)
</sup>|<sup>ON(A,table6) ON(B,table7) ON(C,table8)</sup>|
