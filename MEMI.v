// Diego Jared Jimenez Silva
// Gael Ramses Alvarado Lomelí

module MEMI(
    input [31:0] DR,		// Dirección
    output reg [31:0] INS	// Instruccion de salida
);

reg [7:0] mem[0:999];    // 1000 posiciones que guardan datos de 1 byte

// Leemos el archivo
initial begin
    #50
    $readmemb("datos", mem);
end

// Asignamos
always @(*) begin
	// Recorremos las posiciones siguientes sumando la direccion dada
    INS[31:24] <= mem[DR];
    INS[23:16] <= mem[DR + 1];
    INS[15:8]  <= mem[DR + 2];
    INS[7:0]   <= mem[DR + 3];
end

endmodule
