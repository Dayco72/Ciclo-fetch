//Diego Jared Jimenez Silva
// Gael Ramses Alvarado Lomeli

module ALU(
    input [31:0] A,
    output reg [31:0] RES
);

//En esta ocasion solo sumaremos 4 cada vez, esto para guardar en multiplos de 4 en la memoria
always @(*) begin
        4'b0010: RES = A + 4'b0100;      // ADD
        default: RES = 32'd0;
    endcase
end
endmodule
