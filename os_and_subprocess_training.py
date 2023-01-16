import os
import subprocess


if os.name != "posix":
    print("wrong operating system")
    quit()
    


if not os.path.isdir("/Users/sublimez/test"):
    os.mkdir("/Users/sublimez/test")


os.chdir("/Users/sublimez/test")

for i in range(100):
    with open(f"test_{i}.txt", "w") as f:
        f.write(f"test file number {i}\n")



if os.getcwd() == "/Users/sublimez/test":
    files = os.listdir()
    for file in files:
        os.remove(file)

os.rmdir("/Users/sublimez/test")

os.chdir("..")

print(os.getcwd())


ls = subprocess.run(["ls", "-lh"], capture_output=True, text=True, check=True,)


print(ls.stdout)

print(os.path.isdir("/dev/null"))
