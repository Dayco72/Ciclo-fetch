// Diego Jared Jimenez Silva
// Gael Ramses Alvarado Lomelí

// Modulo Ciclo fetch
module CF(
    input clk,
    output wire[31:0] Inst
);

wire [31:0] CRES, CIN;

ALU     ALInst(.A(CIN), .RES(CRES));
PC      PCInst(.IN(CRES), .CLK(clk), .OUT(CIN));
MEMI    MEInst(.DR(CIN), .INS(Inst));
endmodule

// Testbench
module CFTB();
reg clk;
wire [31:0] Inst;

CF TBInst(.clk(clk), .Inst(Inst));

// Reloj
initial begin
    clk = 0;
    forever #100 clk = ~clk;
end

initial begin
    #1000;
    $stop;
end
endmodule