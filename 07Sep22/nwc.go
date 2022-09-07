// Goal: a very basic lossless compression algorithm (Not Well Compressed - .nwc) written in Go

// Shakespeare's Romeo and Juliet is copied from https://shakespeare.folger.edu/downloads/txt/romeo-and-juliet_TXT_FolgerShakespeare.txt
// Romeo and Juliet is 1% more compact with the nwc algorithm

// The lyrics to We Will Rock You by Queen is 17% more compact with nwc
// For reference the zip format is 39% more compact than the original file

// usage:
// ./nwc compress [filename]
// ./nwc expand [filename]

// explanation:
// imports text file, finds repeated lines or words (breakline or space separated text strings) and creates references to these strings if it would save space, and exports this modified version with a .nwc extension
// (obviously a very basic compression algorithm)

package main

import (
	"bufio"
	"io/ioutil"
	"strings"
	"strconv"
	"fmt"
	"os"
)

var ref_del string = "<*"  // referenced delineator
var rep_del string = "&*"  // repeated delineator

var separator string = ">" // used to separate refs

func input(title string) string {
	fmt.Printf("%v: ", title)
	reader := bufio.NewReader(os.Stdin)
	text, err := reader.ReadString('\n')
	if err != nil { fmt.Printf("read error: %v", err) }
	text = text[:len(text)-1]
	return text
}

func in_slice(val string, slice []string) bool {
	for i := 0; i < len(slice); i++ {
		if val == slice[i] { return true }
	}
	return false
}

func find_rep(values []string, rep []string, file string)  []string {
	for x := 0; x < len(values); x++ {

		// see if its worth finding replicas (need to make sure it shows up enough such that the extra on top is efficient)
		count := strings.Count(file, values[x])
		current_chars := count * len(values[x])
		compressed_chars := len(values[x]) + count * ( len(rep_del) * 2 + 1 ) // does not account for multiple digits in coding

		if current_chars > compressed_chars {

			for y := 0; y < len(values); y++ { // if this line is identical to another line and not in rep [], add it to rep
				if y != x && values[y] == values[x] && !in_slice(values[x], rep) {
					rep = append(rep, values[x])
				}
			}
			
		}

	}
	return rep
}

func unique(s []string) []string {
    inResult := make(map[string]bool)
    var result []string
    for _, str := range s {
        if _, ok := inResult[str]; !ok {
            inResult[str] = true
            result = append(result, str)
        }
    }
    return result
}

func gen_nwc(file string, rep []string)  string {

	new_string := file
	used_rep := rep
	for i := 0; i < len(rep); i++ {
		ref := rep_del + strconv.Itoa(i) + rep_del
		new_string = strings.ReplaceAll(new_string, rep[i], ref)

		// remove from used_reps if not used in condensed string
		if !strings.Contains(new_string, ref) {
			if i+1 < len(used_rep) {
				used_rep = append(used_rep[:i], used_rep[i+1:]...)
			} else {
				used_rep = append(used_rep[:i])
			}
		}
	}

	optimized_rep := strings.Join(unique(used_rep)[:], separator)
	return ref_del + optimized_rep + ref_del + new_string
}

func expand_nwc(file string) string {
    params := strings.Split(file, ref_del)
	expand := strings.ReplaceAll(file, ref_del + params[1] + ref_del, "")
	rep := strings.Split(params[1], separator)

	
	for i := 0; i < len(rep); i++ {
		replace := rep_del + strconv.Itoa(i) + rep_del
		expand = strings.ReplaceAll(expand, replace, rep[i])
	}
	
	return expand
}

func main() {
	// args
	var action string = os.Args[1]
	var filename string = os.Args[2]

	// file handling
	dat, err := ioutil.ReadFile(filename)
	if err != nil { fmt.Printf("file error: %v", err) }
	var file string = string(dat)

	if action == "compress" {
		var rep [] string;

		// generate repetition checks
		check := strings.Split(file, "\n")                 // check for repeated full lines ("\n" separated)
		check = append(check, strings.Split(file, " ")...) // check for repeated full words (" " separated)
		check = append(check, strings.Split(file, ",")...)

		rep = find_rep(check, rep, file)

		// create condensed string
		condensed := gen_nwc(file, rep)

		// console output
		fmt.Printf("compression stats   : %v percent more efficient\n", 100-(100*len(condensed)/len(file)))
		fmt.Printf("compressed/original : %v/%v \n", len(condensed), len(file))
		if (expand_nwc(condensed)==file) {
			fmt.Println("verified lossless")
		}

		// file output 
		err = ioutil.WriteFile(filename + ".nwc", []byte(condensed), 0644)
		if err != nil { fmt.Printf("write error: %v", err) }

	} else if action == "expand" {
		expanded := expand_nwc(file)
		new_filename := strings.ReplaceAll(filename, ".nwc", "")
		err = ioutil.WriteFile(new_filename, []byte(expanded), 0644)
		if err != nil { fmt.Printf("write error: %v", err) }
	}

}