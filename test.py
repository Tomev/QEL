import datetime

backend_name = 'CalibrationHistory\\ibmqx4'

now = datetime.datetime.now()

file_name = backend_name + "_" + now.strftime("%Y-%m-%d_%H-%M") + ".txt"

f = open(file_name, "w+")

f.write("data a")

f.close()

