// Diego Jared Jimenez Silva
// Gael Ramses Alvarado Lomelí

module PC(
    input [31:0] IN,
    input CLK,
    output reg [31:0] OUT
);

always @(posedge CLK) begin	// Cada positivo en el reloj
     OUT <= IN;				// Utilizamos <= para las distintas asignaciones en paralelo
end
	
endmodule
//--------------
