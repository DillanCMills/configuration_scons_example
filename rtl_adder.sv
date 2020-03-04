module adder
(input  var  a, b, ci,
 output var  sum, co);
  timeunit 1ns/1ns;
 
  always_comb
    {co, sum} = a + b + ci;
 
  initial $info("rtl  adder is being used");
  
endmodule:adder
