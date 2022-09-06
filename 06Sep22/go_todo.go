// Goal: a basic todo app written in Go
// note: this is my first Go program so my goal is learning the language rather than optimization

package main

import (
	"bufio"
	"strconv"
	"fmt"
	"os"
)

func in_slice(val string, slice []string) bool {
	for i := 0; i < len(slice); i++ {
		if val == slice[i] { return true }
	}
	return false
}

func remove_from_slice(i int, slice []string) []string {
    return append(slice[:i], slice[i+1:]...)
}

func input(title string) string {
	fmt.Printf("%v: ", title)
	reader := bufio.NewReader(os.Stdin)
	text, err := reader.ReadString('\n')
	if err != nil { fmt.Printf("read error: %v", err) }
	text = text[:len(text)-1]
	return text
}

func main() {
	commands := []string{"list", "add", "remove", "quit"}
	todo := []string{"Go to class", "Finish homework", "Go on a walk"}
	var running bool = true;

	for running {
		var cmd string = input("\naction")

		if in_slice(cmd, commands) {
			if (cmd == commands[0]) {
				fmt.Println("list...")

				for i := 0; i < len(todo); i++ {
					fmt.Printf("%v) %v \n", i+1, todo[i])
				}

			} else if (cmd == commands[1]) {
				var new_todo string = input("new todo")
				todo = append(todo, new_todo)
			} else if (cmd == commands[2]) {
				var remove_string string = input("remove by index")
				remove_index, err := strconv.Atoi(remove_string)
				if err != nil { fmt.Printf("conversion error: %v", err) }

				todo = remove_from_slice(remove_index-1, todo)
			} else if (cmd == commands[3]) {
				running = false
			}
		} else {
			fmt.Printf("unknown command '%v' - help menu\n-------------\noptions: list, add, remove, quit", cmd)
		}
	}

}