import sys
import docker
import sys

def checkErrors():
	if len(sys.argv)!=5:
		return True
	if sys.argv[1]!='-o':
		return True
	if sys.argv[2]!="1" and sys.argv[2]!="2":
		return True
	if sys.argv[3]!='-f':
		return True
	return False

if checkErrors():
	print("Syntax Error!")
	print("Usage: python3 antivirus.py -o <option> -f <fileName>")
	sys.exit(1)

def calUsage(data):
	cpu_count = len(data["cpu_stats"]["cpu_usage"]["percpu_usage"])
	cpu_delta = float(data["cpu_stats"]["cpu_usage"]["total_usage"]) - float(data["precpu_stats"]["cpu_usage"]["total_usage"])
	system_delta = float(data["cpu_stats"]["system_cpu_usage"]) - float(data["precpu_stats"]["system_cpu_usage"])
	
	cpu_percent = cpu_delta / system_delta * 100.0 * cpu_count
	mem_usage = (int(data['memory_stats']['usage']))/(1024*1024)
	
	return cpu_percent,mem_usage

optionFlag=int(sys.argv[2])
iFilePath=sys.argv[4]

try:
	inputFile=open(iFilePath,"r")
except:
	print("Input File: {} not found!".format(iFilePath))
	sys.exit(1)

def part1():

	outputFile=open(iFilePath+".txt","w")
	iFile=inputFile.read()
	
	inputFile.close()
	
	virusFlag=False

	indexes=[]

	for x in range(1,6):
		signFile=open("./Signatures/sig"+str(x)+".txt")
		sFile=signFile.read()
		if sFile in iFile:
			virusFlag=True
			indexes.append(x)

	outputFile.write("Virus : Found\n") if virusFlag else outputFile.write("Virus : Not Found\n")
	outputFile.write("Names of Virus Signatures Found :\n")
	
	for item in indexes:
		outputFile.write("sig"+str(item)+"\n")

	outputFile.close()

def part2():

	inputFile.close()

	outputFile=open(iFilePath+".txt","w")

	dockerFile=open("Dockerfile","w")
	dockerFile.write("FROM java:8\nWORKDIR /\nADD "+iFilePath+" "+iFilePath+"\nEXPOSE 8080\nCMD java -jar "+iFilePath+"\n")
	dockerFile.close()

	client = docker.from_env()
	client.images.build(path="./", tag="test")
	temp = client.images.get("test")
	cOBJ= client.containers.run(temp,detach=True)
	stat = cOBJ.stats(stream=False)
	cOBJ.kill()

	cpu_usage,mem_usage = calUsage(stat)

	if cpu_usage>80 or mem_usage>35:
		outputFile.write("Virus : Found\n")
	else:
		outputFile.write("Virus : Not Found\n")
	outputFile.write("CPU usage (%) :"+str(cpu_usage)+"\n")
	outputFile.write("Memory usage (MB)  :"+str(mem_usage)+"\n")

	outputFile.close()

if optionFlag==1:
	part1()
elif optionFlag==2:
	part2()
else:
	print("Invalid Option!")
	sys.exit(1)