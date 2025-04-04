//Diego Jared Jimenez Silva
// Gael Ramses Alvarado Lomeli

module ALU(
    input [31:0] A,
    output reg [31:0] RES
);

// En esta ocasión solo sumaremos 4 cada vez, esto para guardar en múltiplos de 4 en la memoria
always @(*) begin
    RES = A + 32'd4;	// Corregido: Sumar un valor constante de 32 bits
end
endmodule
