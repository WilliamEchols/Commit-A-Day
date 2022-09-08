/*
Goal: custom esoteric/steganographic language interpreter

Example: The image "trees.png" includes a program that outputs "hello" without looking noticably different than normal pixel art

Specifications:
Composed of 16x16 grid of pixels (image can consist of more but the program is read from the first 16 columns of the first 16 rows)
Instruction sets composed of each 6 digit hex value split in the standard 3 groups (1-## 2-## 3-##)
- Group 1 - command
    - 00: push
    - 01: remove
    - 02: output
    - 03: add
    - 04: subtract
    - 05: if loop is 0, goto first argument, else, goto second argument
- Group 2 - argument
    - holds hex value from 00-FF used in aforementioned commands
- Group 3 - destination
    - contains address in XY format for next command (means program commands can be spread around 16x16 grid in any pattern or create loops throughout any series | also the reason for 16x16 limit)
*/

package main

import (
    "os"
    "image"
    "image/png"
	"strconv"
	"fmt"
)

func hex_to_dec(hex string) int {
	val, err := strconv.ParseInt(hex, 16, 64)
 	if err != nil { panic(err) }
	return int(val)
}

func pop_from_stack(stack []string) []string {
	return append(stack[:len(stack)-1])
}

func main() {
	// init program
	image.RegisterFormat("png", "png", png.Decode, png.DecodeConfig)
	
	// load image
    file, err := os.Open("trees.png") // file name
    if err != nil { panic(err) }
    defer file.Close()
    img, _, err := image.Decode(file)
	if err != nil { panic(err) }

	// construct program from image
	var program [16][16] string;
	for i := 0; i < 16*16; i++ { 
		r, g, b, _ := img.At(i/16, i%16).RGBA()
		program[i%16][i/16] = ("0" + strconv.FormatInt(int64(r), 16))[:2] + (strconv.FormatInt(int64(g), 16) + "0")[:2] + ("0" + strconv.FormatInt(int64(b), 16))[:2]
	}

	// memory and ptr
	pxl_x := 0
	pxl_y := 0
	var stack []string

	// execution loop
	for pxl_x < 15 || pxl_y < 15 {
		c_instruction := program[pxl_x][pxl_y]
		cmd := c_instruction[0:2]
		arg := c_instruction[2:4]
		dest := c_instruction[4:6]

		if (cmd == "00") {        // push
			stack = append(stack, string(arg))
		} else if (cmd == "01") { // remove

			stack = pop_from_stack(stack)
		} else if (cmd == "02") { // output and drop
			fmt.Print(string(hex_to_dec(stack[len(stack)-1])))

			stack = pop_from_stack(stack)
		} else if (cmd == "03") { // add
			stack[len(stack)-2] = string(hex_to_dec(stack[len(stack)-2]) + hex_to_dec(stack[len(stack)-1]))

			stack = pop_from_stack(stack)
		} else if (cmd == "04") { // subtract
			stack[len(stack)-2] = string(hex_to_dec(stack[len(stack)-2]) - hex_to_dec(stack[len(stack)-1]))

			stack = pop_from_stack(stack)
		}

		// goto
		if (cmd == "05" && len(stack) == 0) {
			pxl_x, pxl_y = hex_to_dec(string(arg[0])), hex_to_dec(string(arg[1]))
		} else {
			pxl_x, pxl_y = hex_to_dec(string(dest[0])), hex_to_dec(string(dest[1]))
		}

	}

	fmt.Println()

}