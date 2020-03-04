config rtl_config;
  design rtlLib.top;
  default liblist rtlLib;
endconfig
 
config rtl_config1;
  design testLib.top;
  default liblist rtlLib;
endconfig
 
config rtl_config2;
  design testLib.top;
  default liblist rtlLib testLib;
endconfig
 
  
config cell_config;
  design testLib.top;
  default liblist rtlLib testLib;
  cell adder liblist gateLib;
endconfig
 
config cell_config1;
  design testLib.top;
  default liblist rtlLib testLib;
  cell adder use gateLib.adder;
endconfig
 
config cell_config2;
  design testLib.top;
  default liblist rtlLib testLib;
  cell adder use gateLib.adder_alt;
endconfig
 
  
config inst_config;
  design testLib.top;
  default liblist rtlLib testLib;
  instance top.dut.adder2 liblist gateLib;
endconfig
 
config inst_config1;
  design testLib.top;
  default liblist rtlLib testLib;
  instance top.dut.adder2 use gateLib.adder;
endconfig
 
config inst_config2;
  design testLib.top;
  default liblist rtlLib testLib;
  instance top.dut.adder2 use gateLib.adder_alt;
endconfig
