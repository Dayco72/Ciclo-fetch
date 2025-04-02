// Diego Jared Jimenez Silva
// Gael Ramses Alvarado Lomelí

//Modul
module CF(
	input clk,
	output reg [31:0] Inst
);

wire [31:0] CRES,CIN;

ALU		ALUInst(.A(CIN),.RES(CRES));
PC		PCInst(.IN(CRES),.clk(clk),.OUT(CIN));
MEMI	MEMInst(.DR(CIN[),.INS(Inst));

// Testbench