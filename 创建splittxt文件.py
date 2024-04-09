with open("output.txt", "w") as file:
    for i in range(223):
        line = "scenes/scene-0103 " + str(i) + "\n"
        file.write(line)