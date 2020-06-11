package main

import "os/exec"

func main() {
	//args := []string{"main.py","/Users/binny/go/src/awesomeProject/exec/"}
	//parh:="/Users/binny/go/src/awesomeProject/exec/main.py"
	path_pressure:="/home/pi/projects/python/py2_bmp180/bmp180_example01.py"
	out, err := exec.Command("python2.7", path_pressure).Output()
	if err != nil {
		println("error",err.Error())
		return
	}
	result := string(out)
	println(result)
}

