module adder
(input  var a, b, ci,
 output var sum, co);
  timeunit 1ns/1ns;
 
  logic  n1, n2, n3;
 
  xor    g1 (n1,  a,  b );
  xor #2 g2 (sum, n1, ci);
  and    g3 (n2,  a,  b );
  and    g4 (n3,  n1, ci);
  or  #2 g5 (co,  n2, n3);
 
  initial $info("gate adder is being used");
  
endmodule:adder
