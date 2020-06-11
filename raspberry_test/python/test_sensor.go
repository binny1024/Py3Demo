package main

import "os/exec"

func main() {
	//args := []string{"main.py","/Users/binny/go/src/awesomeProject/exec/"}
	//parh:="/Users/binny/go/src/awesomeProject/exec/main.py"
	path_pressure:="/home/pi/projects/python/test_sensor.sh"
	out, err := exec.Command("sh", path_pressure).Output()
	if err != nil {
		println("error",err.Error())
		return
	}
	result := string(out)
	println("sss", result)
}

