module adder_test
(output var a, b, ci,
 input  var sum1, co1,
 input  var sum2, co2);
  timeunit 1ns/1ns;
 
  initial                 // input stimulus
    begin
      a = 0;
      b = 0;              //              sum   co
      ci = 0;             // should get:   0     0
      #10 a = 1;          // should get:   1     0
      #10 b = 1;          // should get:   0     1
      #10 ci = 1;         // should get:   1     1
      #10 $stop;
      #1000 $finish;
    end
 
  initial                      //response checking
    begin
      //display time in ns, 2 decimal places, 10 char column width
      $timeformat(-9,2," ns",10);
      //print message on change
      $monitor("At %t: \t a=%b  b=%b  ci1=%b  sum1=%b  co1=%b  sum2=%b  co2=%b",
               $realtime, a, b, ci, sum1, co1, sum2, co2);
    end
endmodule
