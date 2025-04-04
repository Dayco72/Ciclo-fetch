// Diego Jared Jimenez Silva
// Gael Ramses Alvarado Lomelí
module PC(
    input [31:0] IN,
    input CLK,
    output reg [31:0] OUT = 32'd0   // Inicializado a 0
);

always @(posedge CLK) begin
    OUT <= IN;
end
	
endmodule
