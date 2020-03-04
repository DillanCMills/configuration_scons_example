module dual_adder (
  input  var a,b,ci, 
  output var sum1, co1,
  output var sum2, co2
);
  timeunit 1ns/1ns;
 
  adder adder1 (.*, 
                .sum(sum1),
                .co (co1 ));
  
  adder adder2 (.*,
                .sum(sum2),
                .co (co2 ));
 
endmodule:dual_adder
