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
|:x:|<sup>table1 table2 table3 A B</sup>|<sup>ON(A,table1) ON(B,table2) CLEAR(table3) HEAVIER(table1,A) HEAVIER(table2,B) HEAVIER(table3,A) HEAVIER(table3,B)</sup>|<sup>ON(A,table3)</sup>|
