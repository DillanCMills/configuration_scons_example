module top;
  timeunit 1ns/1ns;
 
  logic  a, b, ci;
  logic  sum1, co1;
  logic  sum2, co2;
 
  adder_test test (.*);
  dual_adder dut  (.*);
 
endmodule:top
