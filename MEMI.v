// Diego Jared Jimenez Silva
// Gael Ramses Alvarado Lomelí


module MEMI(
	input [31:0] DR, //Direccion
	output [31:0] INS, //Dato de lectura
);

reg [7:0]mem[0:999]; // 1000 posicones que guardan datos de 1byte

//Leemos el archivo
initial
begin 
	#100
	$readmemb("datos", inst.mem); 
end

//Asignamos
always @(*)
begin
	INS <= mem[DR];	
end
endmodule
//--------------